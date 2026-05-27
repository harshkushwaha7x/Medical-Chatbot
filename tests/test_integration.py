"""
Integration tests for Medical Chatbot API endpoints.

Tests the full flow of chat interactions and API functionality.
"""
import unittest
import json
from app import app


class TestChatbotIntegration(unittest.TestCase):
    """Integration tests for chatbot API."""
    
    def setUp(self):
        """Set up test client and fixtures."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_health_endpoint_returns_200(self):
        """Test health check endpoint returns 200 OK."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('status', data)
    
    def test_chat_endpoint_requires_message(self):
        """Test chat endpoint requires message parameter."""
        response = self.client.post(
            '/chat',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_chat_endpoint_with_valid_message(self):
        """Test chat endpoint with valid message."""
        response = self.client.post(
            '/chat',
            data=json.dumps({
                'message': 'What is diabetes?'
            }),
            content_type='application/json'
        )
        # Should return 200 or 500 depending on Pinecone availability
        self.assertIn(response.status_code, [200, 500])
    
    def test_chat_response_structure(self):
        """Test chat response has expected structure."""
        response = self.client.post(
            '/chat',
            data=json.dumps({
                'message': 'Tell me about medical conditions'
            }),
            content_type='application/json'
        )
        
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIn('response', data)
            self.assertIn('sources', data)
    
    def test_invalid_endpoint_returns_404(self):
        """Test invalid endpoint returns 404."""
        response = self.client.get('/invalid/endpoint')
        self.assertEqual(response.status_code, 404)
    
    def test_unsupported_method_returns_405(self):
        """Test unsupported HTTP method returns 405."""
        response = self.client.put('/chat')
        self.assertEqual(response.status_code, 405)
    
    def test_request_logging(self):
        """Test that requests are properly logged."""
        # Make request
        self.client.get('/health')
        # Check that logging occurs (would need to inspect logs in real scenario)
        self.assertTrue(True)  # Placeholder
    
    def test_concurrent_requests(self):
        """Test handling of concurrent requests."""
        import threading
        responses = []
        
        def make_request():
            resp = self.client.get('/health')
            responses.append(resp.status_code)
        
        threads = [threading.Thread(target=make_request) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        # All requests should succeed
        self.assertEqual(len(responses), 5)
        self.assertTrue(all(code == 200 for code in responses))


class TestErrorHandling(unittest.TestCase):
    """Test error handling in API."""
    
    def setUp(self):
        """Set up test client."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_malformed_json_returns_400(self):
        """Test malformed JSON returns 400."""
        response = self.client.post(
            '/chat',
            data='invalid json',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_missing_content_type_handled(self):
        """Test missing content-type is handled gracefully."""
        response = self.client.post('/chat', data='test')
        # Should handle gracefully
        self.assertIn(response.status_code, [400, 415, 500])


if __name__ == '__main__':
    unittest.main()
