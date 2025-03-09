from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager, cache

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128))
    rfid_uid = db.Column(db.String(128), unique=True, index=True)
    is_active = db.Column(db.Boolean, default=True, index=True)
    role = db.Column(db.String(20), default='member', index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships with lazy loading strategies
    memberships = db.relationship('Membership', back_populates='user', lazy='select')
    volunteer_shifts = db.relationship('VolunteerShift', back_populates='volunteer', lazy='dynamic')
    event_registrations = db.relationship('EventRegistration', back_populates='user', lazy='dynamic')
    metrics = db.relationship('VolunteerMetrics', uselist=False, back_populates='volunteer', lazy='joined')
    
    __table_args__ = (
        db.Index('idx_user_auth', 'email', 'is_active'),
        db.Index('idx_user_role', 'role', 'is_active')
    )
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
        
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @classmethod
    def get_by_rfid(cls, rfid_uid):
        """Get user by RFID"""
        return cls.query.filter_by(rfid_uid=rfid_uid, is_active=True).first()

class Membership(db.Model):
    __tablename__ = 'memberships'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    type = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    user = db.relationship('User', back_populates='memberships', lazy='joined')
    
    __table_args__ = (
        db.Index('idx_membership_validation', 'user_id', 'start_date', 'end_date', 'is_active'),
        db.Index('idx_membership_active', 'is_active', 'end_date')
    )
    
    @classmethod
    @cache.memoize(timeout=300)
    def get_active_membership(cls, user_id):
        """Get active membership with caching"""
        return cls.query.filter_by(
            user_id=user_id,
            is_active=True
        ).filter(
            cls.end_date >= datetime.utcnow().date()
        ).first()

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    start_datetime = db.Column(db.DateTime, nullable=False, index=True)
    end_datetime = db.Column(db.DateTime, nullable=False)
    capacity = db.Column(db.Integer)
    location = db.Column(db.String(256))
    event_type = db.Column(db.String(20), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    registrations = db.relationship('EventRegistration', back_populates='event', lazy='dynamic')
    volunteer_shifts = db.relationship('VolunteerShift', back_populates='event', lazy='dynamic')
    
    __table_args__ = (
        db.Index('idx_event_date_type', 'start_datetime', 'event_type'),
        db.Index('idx_event_date_range', 'start_datetime', 'end_datetime')
    )
    
    @property
    @cache.memoize(timeout=60)
    def available_spots(self):
        """Get available spots with short-term caching"""
        if not self.capacity:
            return float('inf')
        return self.capacity - self.registrations.count()

class EventRegistration(db.Model):
    __tablename__ = 'event_registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    registration_time = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='registered')
    check_in_time = db.Column(db.DateTime)
    
    event = db.relationship('Event', back_populates='registrations', lazy='joined')
    user = db.relationship('User', back_populates='event_registrations', lazy='joined')
    
    __table_args__ = (
        db.Index('idx_registration_lookup', 'event_id', 'user_id', 'status'),
        db.Index('idx_registration_status', 'status', 'registration_time')
    )

class VolunteerShift(db.Model):
    __tablename__ = 'volunteer_shifts'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), index=True)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='scheduled')
    priority_score = db.Column(db.Float, default=0.0)
    
    event = db.relationship('Event', back_populates='volunteer_shifts', lazy='joined')
    volunteer = db.relationship('User', back_populates='volunteer_shifts', lazy='joined')
    
    __table_args__ = (
        db.Index('idx_shift_scheduling', 'volunteer_id', 'start_time', 'status', 'priority_score'),
        db.Index('idx_shift_time_range', 'start_time', 'end_time', 'status')
    )

class VolunteerMetrics(db.Model):
    __tablename__ = 'volunteer_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    total_hours = db.Column(db.Float, default=0.0)
    reliability_score = db.Column(db.Float, default=1.0)
    seniority_score = db.Column(db.Float, default=0.0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    volunteer = db.relationship('User', back_populates='metrics', lazy='joined')
    
    __table_args__ = (
        db.Index('idx_metrics_scores', 'reliability_score', 'seniority_score'),
    )
    
    @classmethod
    @cache.memoize(timeout=3600)
    def get_top_volunteers(cls, limit=10):
        """Get top volunteers based on combined metrics with caching"""
        return cls.query.order_by(
            (cls.reliability_score * 0.4 + cls.seniority_score * 0.6).desc()
        ).limit(limit).all()

@login_manager.user_loader
@cache.memoize(timeout=300)
def load_user(user_id):
    """Load user with caching"""
    return User.query.get(int(user_id))
