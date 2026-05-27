"""
Rate limiting middleware to prevent API abuse.

This module provides rate limiting functionality for the Medical Chatbot API.
"""
from flask import request, jsonify
from functools import wraps
from datetime import datetime, timedelta
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """Rate limiter to protect API endpoints from abuse."""
    
    def __init__(self, max_requests=100, time_window_minutes=60):
        """Initialize rate limiter.
        
        Args:
            max_requests: Maximum requests allowed in time window
            time_window_minutes: Time window in minutes
        """
        self.max_requests = max_requests
        self.time_window = timedelta(minutes=time_window_minutes)
        self.requests = defaultdict(list)
    
    def is_rate_limited(self, client_id):
        """Check if client has exceeded rate limit.
        
        Args:
            client_id: Unique identifier for client (IP address)
            
        Returns:
            bool: True if rate limited, False otherwise
        """
        now = datetime.now()
        
        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.time_window
        ]
        
        # Check limit
        if len(self.requests[client_id]) >= self.max_requests:
            logger.warning(f"Rate limit exceeded for {client_id}")
            return True
        
        # Add current request
        self.requests[client_id].append(now)
        return False


# Global rate limiter instance
rate_limiter = RateLimiter(max_requests=100, time_window_minutes=60)


def rate_limit(f):
    """Decorator to apply rate limiting to endpoints."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_id = request.remote_addr
        
        if rate_limiter.is_rate_limited(client_id):
            logger.warning(f"Rate limited request from {client_id}")
            return jsonify({
                "error": "Rate limit exceeded",
                "message": "Too many requests. Please try again later."
            }), 429
        
        return f(*args, **kwargs)
    
    return decorated_function
