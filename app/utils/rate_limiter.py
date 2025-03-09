"""Rate limiting utility for RHT RFID system"""
from functools import wraps
from flask import request, current_app
from redis import Redis
import time

class RateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client
        
    def limit(self, key_prefix, limit=100, period=60):
        """
        Rate limiting decorator
        :param key_prefix: Prefix for Redis key
        :param limit: Number of requests allowed per period
        :param period: Time period in seconds
        """
        def decorator(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                key = f"{key_prefix}:{request.remote_addr}"
                current = int(time.time())
                period_start = current - (current % period)
                
                with self.redis.pipeline() as pipe:
                    # Add current timestamp and cleanup old entries
                    pipe.zadd(key, {str(current): current})
                    pipe.zremrangebyscore(key, 0, period_start)
                    # Count requests in current period and set expiry
                    pipe.zcard(key)
                    pipe.expire(key, period)
                    _, _, request_count, _ = pipe.execute()
                
                if request_count > limit:
                    return {'error': 'Too many requests'}, 429
                
                return f(*args, **kwargs)
            return wrapped
        return decorator

# Specialized rate limiters for different endpoints
def limit_login_attempts(redis_client, max_attempts=5, period=300):
    """Rate limit login attempts"""
    return RateLimiter(redis_client).limit(
        'login',
        limit=max_attempts,
        period=period
    )

def limit_rfid_scans(redis_client, max_scans=20, period=60):
    """Rate limit RFID scan attempts"""
    return RateLimiter(redis_client).limit(
        'rfid_scan',
        limit=max_scans,
        period=period
    )

def limit_api_calls(redis_client, max_calls=1000, period=3600):
    """Rate limit API calls"""
    return RateLimiter(redis_client).limit(
        'api',
        limit=max_calls,
        period=period
    )
