"""
Test cases for Flask application endpoints.
"""
import unittest
from app import app


class TestChatbotAPI(unittest.TestCase):
    """Test API endpoints."""
    
    def setUp(self):
        """Set up test client."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
    
    def test_chat_endpoint_missing_message(self):
        """Test chat endpoint with missing message."""
        response = self.client.post('/chat', json={})
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
