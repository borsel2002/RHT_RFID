import logging
from logging.handlers import RotatingFileHandler
import traceback
from functools import wraps
from flask import current_app, jsonify, request
import sentry_sdk
from pythonjsonlogger import jsonlogger
from datetime import datetime

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['timestamp'] = datetime.utcnow().isoformat()
        log_record['level'] = record.levelname
        log_record['logger'] = record.name

def setup_logging(app):
    """Configure application logging"""
    if not app.debug:
        # Set up JSON formatter
        formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')
        
        # File handler for all logs
        file_handler = RotatingFileHandler(
            'logs/app.log',
            maxBytes=10485760,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        
        # Error file handler
        error_handler = RotatingFileHandler(
            'logs/error.log',
            maxBytes=10485760,
            backupCount=10
        )
        error_handler.setFormatter(formatter)
        error_handler.setLevel(logging.ERROR)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.addHandler(file_handler)
        root_logger.addHandler(error_handler)
        root_logger.setLevel(logging.INFO)
        
        # Configure Flask logger
        app.logger.addHandler(file_handler)
        app.logger.addHandler(error_handler)
        app.logger.setLevel(logging.INFO)
        
        # Initialize Sentry
        if app.config.get('SENTRY_DSN'):
            sentry_sdk.init(
                dsn=app.config['SENTRY_DSN'],
                environment=app.config.get('ENV', 'production'),
                traces_sample_rate=1.0
            )
    
    return app.logger

def handle_error(error):
    """Generic error handler for all exceptions"""
    error_context = {
        'error_message': str(error),
        'error_type': error.__class__.__name__,
        'traceback': traceback.format_exc(),
        'endpoint': request.endpoint,
        'method': request.method,
        'url': request.url,
        'ip': request.remote_addr,
        'user_agent': str(request.user_agent)
    }
    
    # Log the error
    current_app.logger.error('Exception occurred', extra=error_context)
    
    # Report to Sentry if in production
    if not current_app.debug and current_app.config.get('SENTRY_DSN'):
        sentry_sdk.capture_exception(error)
    
    # Return appropriate response
    if request.is_json:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(error) if current_app.debug else 'An unexpected error occurred'
        }), 500
    else:
        return 'Internal Server Error', 500

def log_function_call(f):
    """Decorator to log function calls with timing"""
    @wraps(f)
    def decorated(*args, **kwargs):
        start_time = datetime.utcnow()
        
        try:
            result = f(*args, **kwargs)
            end_time = datetime.utcnow()
            
            current_app.logger.info(
                f'Function call completed',
                extra={
                    'function': f.__name__,
                    'duration_ms': (end_time - start_time).total_seconds() * 1000,
                    'success': True
                }
            )
            return result
            
        except Exception as e:
            end_time = datetime.utcnow()
            current_app.logger.error(
                'Function call failed',
                extra={
                    'function': f.__name__,
                    'duration_ms': (end_time - start_time).total_seconds() * 1000,
                    'error': str(e),
                    'traceback': traceback.format_exc()
                }
            )
            raise
    
    return decorated
