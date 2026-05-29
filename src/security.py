"""
CORS and security headers configuration.

Provides configuration for Cross-Origin Resource Sharing (CORS)
and security headers to protect against common web vulnerabilities.
"""
import logging
from flask import Flask
from flask_cors import CORS

logger = logging.getLogger(__name__)


class SecurityHeaders:
    """Security headers configuration."""
    
    # Security headers to add to all responses
    HEADERS = {
        # Prevent clickjacking
        'X-Frame-Options': 'DENY',
        
        # Prevent MIME type sniffing
        'X-Content-Type-Options': 'nosniff',
        
        # Enable XSS protection
        'X-XSS-Protection': '1; mode=block',
        
        # Content Security Policy
        'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
        
        # Strict Transport Security
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        
        # Prevent information disclosure
        'X-Powered-By': '',
        'Server': 'Medical Chatbot/1.0',
        
        # Referrer Policy
        'Referrer-Policy': 'strict-origin-when-cross-origin'
    }
    
    @staticmethod
    def apply_headers(response):
        """Apply security headers to response.
        
        Args:
            response: Flask response object
            
        Returns:
            Modified response with security headers
        """
        for header, value in SecurityHeaders.HEADERS.items():
            response.headers[header] = value
        
        logger.debug("Security headers applied")
        return response


class CORSConfiguration:
    """CORS configuration for the application."""
    
    # Allowed origins for CORS
    ALLOWED_ORIGINS = [
        'http://localhost:3000',
        'http://localhost:5000',
        'https://yourdomain.com',
    ]
    
    # CORS options
    CORS_OPTIONS = {
        'origins': ALLOWED_ORIGINS,
        'methods': ['GET', 'POST', 'OPTIONS'],
        'allow_headers': ['Content-Type', 'Authorization'],
        'expose_headers': ['Content-Type'],
        'supports_credentials': True,
        'max_age': 3600
    }
    
    @staticmethod
    def configure_cors(app: Flask):
        """Configure CORS for Flask application.
        
        Args:
            app: Flask application instance
        """
        CORS(app, resources={
            r"/api/*": CORSConfiguration.CORS_OPTIONS
        })
        logger.info("CORS configured successfully")
    
    @staticmethod
    def is_origin_allowed(origin: str) -> bool:
        """Check if origin is allowed.
        
        Args:
            origin: Origin to check
            
        Returns:
            True if origin is allowed
        """
        return origin in CORSConfiguration.ALLOWED_ORIGINS


def configure_security(app: Flask):
    """Configure all security settings for application.
    
    Args:
        app: Flask application instance
    """
    # Configure CORS
    CORSConfiguration.configure_cors(app)
    
    # Add security headers to all responses
    @app.after_request
    def add_security_headers(response):
        """Add security headers to response."""
        return SecurityHeaders.apply_headers(response)
    
    logger.info("Security configuration completed")


class SecurityPolicy:
    """Security policy enforcement."""
    
    # Content Security Policy
    CSP = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:"
    
    # Allowed file types for upload
    ALLOWED_FILE_TYPES = ['.pdf', '.txt', '.docx']
    
    # Maximum file size (10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    @staticmethod
    def is_file_allowed(filename: str) -> bool:
        """Check if file type is allowed.
        
        Args:
            filename: Name of file
            
        Returns:
            True if file type is allowed
        """
        import os
        _, ext = os.path.splitext(filename)
        return ext.lower() in SecurityPolicy.ALLOWED_FILE_TYPES
    
    @staticmethod
    def is_file_size_valid(file_size: int) -> bool:
        """Check if file size is valid.
        
        Args:
            file_size: Size of file in bytes
            
        Returns:
            True if file size is within limits
        """
        return file_size <= SecurityPolicy.MAX_FILE_SIZE
