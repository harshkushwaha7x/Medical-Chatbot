"""
Security validation tests.

Tests for input validation, sanitization, and security headers.
"""
import unittest
from src.validation import InputValidator, InputSanitizer, validate_request_data
from src.security import SecurityHeaders, CORSConfiguration


class TestInputValidation(unittest.TestCase):
    """Test input validation functionality."""
    
    def test_validate_empty_message(self):
        """Test that empty messages are rejected."""
        is_valid, error = InputValidator.validate_message("")
        self.assertFalse(is_valid)
        self.assertIn("empty", error.lower())
    
    def test_validate_long_message(self):
        """Test that very long messages are rejected."""
        long_message = "a" * 10000
        is_valid, error = InputValidator.validate_message(long_message)
        self.assertFalse(is_valid)
        self.assertIn("exceeds", error.lower())
    
    def test_validate_xss_attempt(self):
        """Test that XSS attempts are detected."""
        xss_message = "<script>alert('xss')</script>"
        is_valid, error = InputValidator.validate_message(xss_message)
        self.assertFalse(is_valid)
        self.assertIn("suspicious", error.lower())
    
    def test_validate_sql_injection_attempt(self):
        """Test that SQL injection attempts are detected."""
        sql_message = "'; DROP TABLE users; --"
        is_valid, error = InputValidator.validate_message(sql_message)
        self.assertFalse(is_valid)
        self.assertIn("suspicious", error.lower())
    
    def test_validate_legitimate_message(self):
        """Test that legitimate messages pass validation."""
        message = "What are the symptoms of diabetes?"
        is_valid, error = InputValidator.validate_message(message)
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_validate_email_valid(self):
        """Test valid email validation."""
        is_valid, error = InputValidator.validate_email("test@example.com")
        self.assertTrue(is_valid)
    
    def test_validate_email_invalid(self):
        """Test invalid email validation."""
        is_valid, error = InputValidator.validate_email("invalid-email")
        self.assertFalse(is_valid)
    
    def test_sanitize_string_removes_tags(self):
        """Test that HTML tags are sanitized."""
        input_str = "<script>alert('xss')</script>"
        sanitized = InputValidator.sanitize_string(input_str)
        self.assertNotIn("<script>", sanitized)
        self.assertIn("&lt;", sanitized)


class TestInputSanitization(unittest.TestCase):
    """Test input sanitization functionality."""
    
    def test_sanitize_message_returns_string(self):
        """Test that sanitize_message returns a string."""
        result = InputSanitizer.sanitize_message("Hello world")
        self.assertIsInstance(result, str)
    
    def test_sanitize_query_limits_length(self):
        """Test that query sanitization limits length."""
        long_query = "a" * 5000
        result = InputSanitizer.sanitize_query(long_query)
        self.assertLessEqual(len(result), 1000)
    
    def test_sanitize_removes_special_chars(self):
        """Test that dangerous characters are removed."""
        dangerous = "Normal text <script>bad</script>"
        result = InputSanitizer.sanitize_message(dangerous)
        self.assertNotIn("<script>", result)


class TestRequestDataValidation(unittest.TestCase):
    """Test request data validation."""
    
    def test_validate_request_missing_message(self):
        """Test that request without message is rejected."""
        data = {}
        is_valid, error = validate_request_data(data)
        self.assertFalse(is_valid)
        self.assertIn("required", error.lower())
    
    def test_validate_request_with_message(self):
        """Test that valid request passes validation."""
        data = {"message": "Hello"}
        is_valid, error = validate_request_data(data)
        self.assertTrue(is_valid)
    
    def test_validate_request_non_dict(self):
        """Test that non-dict data is rejected."""
        is_valid, error = validate_request_data("not a dict")
        self.assertFalse(is_valid)


class TestSecurityHeaders(unittest.TestCase):
    """Test security headers configuration."""
    
    def test_security_headers_contain_frame_options(self):
        """Test that X-Frame-Options header is present."""
        self.assertIn('X-Frame-Options', SecurityHeaders.HEADERS)
    
    def test_security_headers_contain_csp(self):
        """Test that Content-Security-Policy header is present."""
        self.assertIn('Content-Security-Policy', SecurityHeaders.HEADERS)
    
    def test_security_headers_contain_hsts(self):
        """Test that HSTS header is present."""
        self.assertIn('Strict-Transport-Security', SecurityHeaders.HEADERS)


class TestCORSConfiguration(unittest.TestCase):
    """Test CORS configuration."""
    
    def test_cors_allowed_origin_valid(self):
        """Test that valid origins are allowed."""
        is_allowed = CORSConfiguration.is_origin_allowed('http://localhost:5000')
        self.assertTrue(is_allowed)
    
    def test_cors_disallowed_origin_invalid(self):
        """Test that invalid origins are rejected."""
        is_allowed = CORSConfiguration.is_origin_allowed('http://evil.com')
        self.assertFalse(is_allowed)


if __name__ == '__main__':
    unittest.main()
