"""
Input validation and sanitization module.

Provides utilities for validating and sanitizing user inputs
to prevent injection attacks and malicious payloads.
"""
import re
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class InputValidator:
    """Validates and sanitizes user inputs."""
    
    # Patterns for validation
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    URL_PATTERN = r'^https?://[^\s]+$'
    SAFE_MESSAGE_PATTERN = r'^[a-zA-Z0-9\s\.\,\!\?\-\'\"]+$'
    
    # Maximum lengths
    MAX_MESSAGE_LENGTH = 5000
    MAX_QUERY_LENGTH = 1000
    
    @staticmethod
    def validate_message(message: str) -> tuple[bool, Optional[str]]:
        """Validate chat message.
        
        Args:
            message: User message to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not message:
            return False, "Message cannot be empty"
        
        if not isinstance(message, str):
            return False, "Message must be a string"
        
        # Check length
        if len(message) > InputValidator.MAX_MESSAGE_LENGTH:
            return False, f"Message exceeds maximum length of {InputValidator.MAX_MESSAGE_LENGTH}"
        
        # Check for suspicious patterns (basic XSS/injection detection)
        suspicious_patterns = [
            r'<script',
            r'javascript:',
            r'onerror=',
            r'onload=',
            r'sql',
            r'drop table',
            r'delete from'
        ]
        
        message_lower = message.lower()
        for pattern in suspicious_patterns:
            if re.search(pattern, message_lower):
                logger.warning(f"Suspicious pattern detected: {pattern}")
                return False, "Message contains suspicious content"
        
        return True, None
    
    @staticmethod
    def validate_email(email: str) -> tuple[bool, Optional[str]]:
        """Validate email address.
        
        Args:
            email: Email to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not email:
            return False, "Email cannot be empty"
        
        if not re.match(InputValidator.EMAIL_PATTERN, email):
            return False, "Invalid email format"
        
        if len(email) > 254:  # RFC 5321
            return False, "Email is too long"
        
        return True, None
    
    @staticmethod
    def sanitize_string(text: str, max_length: int = 1000) -> str:
        """Sanitize string input.
        
        Args:
            text: Text to sanitize
            max_length: Maximum length
            
        Returns:
            Sanitized string
        """
        if not isinstance(text, str):
            return ""
        
        # Remove null bytes
        text = text.replace('\x00', '')
        
        # Strip whitespace
        text = text.strip()
        
        # Limit length
        text = text[:max_length]
        
        # Escape HTML special characters
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&#x27;')
        
        return text
    
    @staticmethod
    def validate_api_key(key: str) -> tuple[bool, Optional[str]]:
        """Validate API key format.
        
        Args:
            key: API key to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not key:
            return False, "API key cannot be empty"
        
        if len(key) < 16:
            return False, "API key is too short"
        
        if len(key) > 256:
            return False, "API key is too long"
        
        # Check for valid characters (alphanumeric and common separators)
        if not re.match(r'^[a-zA-Z0-9\-_]+$', key):
            return False, "API key contains invalid characters"
        
        return True, None


class InputSanitizer:
    """Sanitizes user inputs."""
    
    @staticmethod
    def sanitize_message(message: str) -> str:
        """Sanitize user message.
        
        Args:
            message: Message to sanitize
            
        Returns:
            Sanitized message
        """
        # Validate first
        is_valid, error = InputValidator.validate_message(message)
        if not is_valid:
            logger.warning(f"Invalid message: {error}")
            return ""
        
        # Sanitize
        return InputValidator.sanitize_string(message, max_length=5000)
    
    @staticmethod
    def sanitize_query(query: str) -> str:
        """Sanitize database query.
        
        Args:
            query: Query to sanitize
            
        Returns:
            Sanitized query
        """
        return InputValidator.sanitize_string(query, max_length=1000)


def validate_request_data(data: dict) -> tuple[bool, Optional[str]]:
    """Validate request data.
    
    Args:
        data: Request data dictionary
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(data, dict):
        return False, "Request data must be a dictionary"
    
    if 'message' not in data:
        return False, "Message field is required"
    
    is_valid, error = InputValidator.validate_message(data['message'])
    if not is_valid:
        return False, error
    
    return True, None
