from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_caching import Cache
from flask_mail import Mail
from flask_qrcode import QRcode
from flask_wtf.csrf import CSRFProtect
from config import config
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
cache = Cache()
mail = Mail()
csrf = CSRFProtect()
qrcode = QRcode()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    qrcode.init_app(app)
    
    # Configure Sentry for production
    if not app.debug:
        sentry_sdk.init(
            dsn=app.config.get('SENTRY_DSN'),
            integrations=[FlaskIntegration()],
            traces_sample_rate=1.0
        )
    
    # Security headers middleware
    @app.after_request
    def add_security_headers(response):
        for header, value in app.config['SECURITY_HEADERS'].items():
            response.headers[header] = value
        return response
    
    # Register blueprints
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    from app.volunteer import volunteer as volunteer_blueprint
    app.register_blueprint(volunteer_blueprint, url_prefix='/volunteer')
    
    from app.events import events as events_blueprint
    app.register_blueprint(events_blueprint, url_prefix='/events')
    
    return app
