"""
Environment-specific security settings.
"""
import os
from typing import Dict, Any


class SecurityConfig:
    """Base security configuration."""
    
    # Session settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600
    
    # Password settings
    MIN_PASSWORD_LENGTH = 12
    REQUIRE_UPPERCASE = True
    REQUIRE_DIGITS = True
    REQUIRE_SPECIAL_CHARS = True
    
    # API settings
    API_RATE_LIMIT = 100  # requests per hour
    API_TIMEOUT = 30  # seconds
    
    # CORS settings
    ALLOWED_ORIGINS = []
    
    # File upload
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES = ['.pdf', '.txt']


class DevelopmentSecurityConfig(SecurityConfig):
    """Security configuration for development environment."""
    
    SESSION_COOKIE_SECURE = False  # Allow HTTP
    DEBUG = True
    TESTING = False
    
    # Relaxed settings for development
    API_RATE_LIMIT = 1000
    ALLOWED_ORIGINS = [
        'http://localhost:3000',
        'http://localhost:5000',
        'http://127.0.0.1:3000',
    ]


class ProductionSecurityConfig(SecurityConfig):
    """Security configuration for production environment."""
    
    SESSION_COOKIE_SECURE = True  # HTTPS only
    DEBUG = False
    TESTING = False
    
    # Strict settings for production
    API_RATE_LIMIT = 100
    ALLOWED_ORIGINS = [
        'https://yourdomain.com',
        'https://www.yourdomain.com',
    ]


class TestingSecurityConfig(SecurityConfig):
    """Security configuration for testing environment."""
    
    SESSION_COOKIE_SECURE = False
    DEBUG = True
    TESTING = True
    
    # Permissive for testing
    API_RATE_LIMIT = 10000
    ALLOWED_ORIGINS = ['*']


def get_security_config(environment: str = None) -> SecurityConfig:
    """Get security configuration for environment.
    
    Args:
        environment: Environment name (development/production/testing)
        
    Returns:
        SecurityConfig instance
    """
    if environment is None:
        environment = os.environ.get('FLASK_ENV', 'development')
    
    configs = {
        'development': DevelopmentSecurityConfig(),
        'production': ProductionSecurityConfig(),
        'testing': TestingSecurityConfig(),
    }
    
    return configs.get(environment, DevelopmentSecurityConfig())


def get_security_settings() -> Dict[str, Any]:
    """Get all security settings.
    
    Returns:
        Dictionary of security settings
    """
    config = get_security_config()
    
    return {
        'session_cookie_secure': config.SESSION_COOKIE_SECURE,
        'session_cookie_httponly': config.SESSION_COOKIE_HTTPONLY,
        'session_cookie_samesite': config.SESSION_COOKIE_SAMESITE,
        'permanent_session_lifetime': config.PERMANENT_SESSION_LIFETIME,
        'min_password_length': config.MIN_PASSWORD_LENGTH,
        'require_uppercase': config.REQUIRE_UPPERCASE,
        'require_digits': config.REQUIRE_DIGITS,
        'require_special_chars': config.REQUIRE_SPECIAL_CHARS,
        'api_rate_limit': config.API_RATE_LIMIT,
        'api_timeout': config.API_TIMEOUT,
        'allowed_origins': config.ALLOWED_ORIGINS,
        'max_file_size': config.MAX_FILE_SIZE,
        'allowed_file_types': config.ALLOWED_FILE_TYPES,
    }
