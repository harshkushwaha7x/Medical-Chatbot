"""
Enhanced error handling module.

Provides comprehensive error handling, logging, and recovery mechanisms.
"""
import logging
import traceback
from functools import wraps
from typing import Callable, Any, Optional
from flask import jsonify

logger = logging.getLogger(__name__)


class ChatbotError(Exception):
    """Base exception for chatbot errors."""
    
    def __init__(self, message: str, code: int = 500, details: Optional[dict] = None):
        """Initialize error.
        
        Args:
            message: Error message
            code: HTTP status code
            details: Additional error details
        """
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(ChatbotError):
    """Raised when validation fails."""
    
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message, code=400, details=details)


class AuthenticationError(ChatbotError):
    """Raised when authentication fails."""
    
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message, code=401, details=details)


class NotFoundError(ChatbotError):
    """Raised when resource is not found."""
    
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message, code=404, details=details)


class RateLimitError(ChatbotError):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message, code=429, details=details)


class InternalServerError(ChatbotError):
    """Raised for internal server errors."""
    
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message, code=500, details=details)


class ExternalAPIError(ChatbotError):
    """Raised when external API call fails."""
    
    def __init__(self, message: str, api_name: str, details: Optional[dict] = None):
        """Initialize external API error.
        
        Args:
            message: Error message
            api_name: Name of external API
            details: Additional error details
        """
        self.api_name = api_name
        super().__init__(message, code=503, details=details)


class ErrorHandler:
    """Handles errors and exceptions."""
    
    @staticmethod
    def handle_error(error: Exception) -> tuple[dict, int]:
        """Handle error and return response.
        
        Args:
            error: Exception to handle
            
        Returns:
            Tuple of (response_dict, status_code)
        """
        if isinstance(error, ChatbotError):
            logger.error(f"{error.__class__.__name__}: {error.message}", extra=error.details)
            return {
                'error': error.message,
                'type': error.__class__.__name__,
                'details': error.details
            }, error.code
        
        # Handle unexpected errors
        logger.error(f"Unexpected error: {str(error)}")
        logger.error(traceback.format_exc())
        
        return {
            'error': 'An unexpected error occurred',
            'type': 'InternalServerError'
        }, 500
    
    @staticmethod
    def handle_external_api_error(api_name: str, error: Exception) -> None:
        """Log external API error.
        
        Args:
            api_name: Name of external API
            error: Exception from API
            
        Raises:
            ExternalAPIError
        """
        logger.error(f"{api_name} API error: {str(error)}")
        raise ExternalAPIError(
            message=f"Failed to communicate with {api_name}",
            api_name=api_name,
            details={'original_error': str(error)}
        )


def handle_errors(f: Callable) -> Callable:
    """Decorator to handle errors in endpoints.
    
    Args:
        f: Function to decorate
        
    Returns:
        Decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs) -> tuple[dict, int]:
        try:
            return f(*args, **kwargs)
        except ChatbotError as e:
            response, code = ErrorHandler.handle_error(e)
            return jsonify(response), code
        except Exception as e:
            response, code = ErrorHandler.handle_error(e)
            return jsonify(response), code
    
    return decorated_function


class RecoveryMechanism:
    """Handles error recovery and retries."""
    
    @staticmethod
    def retry(max_attempts: int = 3, backoff_factor: float = 2.0):
        """Decorator for retry logic.
        
        Args:
            max_attempts: Maximum retry attempts
            backoff_factor: Exponential backoff factor
            
        Returns:
            Decorator function
        """
        def decorator(f: Callable) -> Callable:
            @wraps(f)
            def wrapper(*args, **kwargs) -> Any:
                import time
                
                last_exception = None
                for attempt in range(max_attempts):
                    try:
                        return f(*args, **kwargs)
                    except Exception as e:
                        last_exception = e
                        if attempt < max_attempts - 1:
                            wait_time = (backoff_factor ** attempt)
                            logger.warning(
                                f"Attempt {attempt + 1} failed. "
                                f"Retrying in {wait_time}s..."
                            )
                            time.sleep(wait_time)
                
                logger.error(f"All {max_attempts} attempts failed")
                raise last_exception
            
            return wrapper
        return decorator
