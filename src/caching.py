"""
Request caching system for improved performance.

This module implements caching for frequently requested queries
to reduce API calls and improve response times.
"""
import hashlib
import json
from functools import wraps
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class ResponseCache:
    """Simple in-memory cache for API responses."""
    
    def __init__(self, ttl_minutes=30):
        """Initialize cache.
        
        Args:
            ttl_minutes: Time to live for cache entries in minutes
        """
        self.cache = {}
        self.ttl = timedelta(minutes=ttl_minutes)
    
    def get_cache_key(self, query):
        """Generate cache key from query.
        
        Args:
            query: Query string
            
        Returns:
            str: Hash of query
        """
        return hashlib.sha256(query.encode()).hexdigest()
    
    def get(self, key):
        """Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value if exists and not expired, None otherwise
        """
        if key in self.cache:
            data, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.ttl:
                logger.info(f"Cache hit for key {key}")
                return data
            else:
                del self.cache[key]
                logger.info(f"Cache expired for key {key}")
        
        return None
    
    def set(self, key, value):
        """Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        self.cache[key] = (value, datetime.now())
        logger.info(f"Cached response for key {key}")
    
    def clear(self):
        """Clear all cache entries."""
        self.cache.clear()
        logger.info("Cache cleared")


# Global cache instance
response_cache = ResponseCache(ttl_minutes=30)


def cacheable(f):
    """Decorator to add caching to endpoints."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Create cache key from request data
        cache_key = response_cache.get_cache_key(
            str(args) + str(kwargs)
        )
        
        # Check cache
        cached_response = response_cache.get(cache_key)
        if cached_response:
            return cached_response
        
        # Get fresh response
        response = f(*args, **kwargs)
        
        # Cache response
        response_cache.set(cache_key, response)
        
        return response
    
    return decorated_function
