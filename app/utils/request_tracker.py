"""Request tracking utility for RHT RFID system"""
from functools import wraps
from flask import request, g, current_app
import time
import uuid
from datetime import datetime

def generate_request_id():
    """Generate a unique request ID"""
    return str(uuid.uuid4())

def track_request(f):
    """Decorator to track request metrics"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        # Start timing
        start_time = time.time()
        
        # Generate request ID and store in g
        request_id = generate_request_id()
        g.request_id = request_id
        
        # Track request start
        current_app.logger.info(
            'Request started',
            extra={
                'request_id': request_id,
                'method': request.method,
                'path': request.path,
                'remote_addr': request.remote_addr,
                'user_agent': str(request.user_agent)
            }
        )
        
        try:
            response = f(*args, **kwargs)
            duration = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            # Track successful request
            current_app.logger.info(
                'Request completed',
                extra={
                    'request_id': request_id,
                    'duration_ms': duration,
                    'status_code': response.status_code if hasattr(response, 'status_code') else 'unknown'
                }
            )
            
            return response
            
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            
            # Track failed request
            current_app.logger.error(
                'Request failed',
                extra={
                    'request_id': request_id,
                    'duration_ms': duration,
                    'error': str(e),
                    'error_type': e.__class__.__name__
                }
            )
            raise
            
    return wrapped
