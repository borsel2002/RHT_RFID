from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from app.models import User, db
from app.auth.forms import LoginForm, RegistrationForm, TwoFactorForm
import pyotp
from datetime import datetime
import hashlib
from functools import wraps
from app import cache

auth = Blueprint('auth', __name__)

def require_2fa(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and not session.get('2fa_verified'):
            return redirect(url_for('auth.two_factor_auth'))
        return f(*args, **kwargs)
    return decorated_function

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.verify_password(form.password.data):
            if user.two_factor_secret:
                session['temp_user_id'] = user.id
                return redirect(url_for('auth.two_factor_auth'))
            
            login_user(user, remember=form.remember_me.data)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.index')
            return redirect(next_page)
        flash('Invalid email or password', 'error')
    return render_template('auth/login.html', form=form)

@auth.route('/two-factor', methods=['GET', 'POST'])
def two_factor_auth():
    if 'temp_user_id' not in session:
        return redirect(url_for('auth.login'))
        
    form = TwoFactorForm()
    if form.validate_on_submit():
        user = User.query.get(session['temp_user_id'])
        totp = pyotp.TOTP(user.two_factor_secret)
        
        if totp.verify(form.token.data):
            login_user(user)
            session['2fa_verified'] = True
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            session.pop('temp_user_id', None)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.index')
            return redirect(next_page)
        flash('Invalid 2FA token', 'error')
    return render_template('auth/two_factor.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data.lower(),
            two_factor_secret=pyotp.random_base32()
        )
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('2fa_verified', None)
    return redirect(url_for('main.index'))

@auth.route('/rfid-auth/<rfid_uid>')
@cache.memoize(timeout=30)  # Cache to prevent brute force attempts
def rfid_auth(rfid_uid):
    """Authenticate user via RFID"""
    salt = current_app.config['RFID_HASH_SALT']
    hashed_uid = hashlib.sha256(f"{rfid_uid}{salt}".encode()).hexdigest()
    
    user = User.query.filter_by(rfid_uid_hash=hashed_uid).first()
    if not user:
        return jsonify({'status': 'error', 'message': 'Invalid RFID'}), 401
        
    login_user(user)
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'Authentication successful',
        'redirect_url': url_for('main.index')
    })
