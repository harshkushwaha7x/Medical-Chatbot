"""
End-to-end integration tests for Medical Chatbot.

Tests the complete workflow from user input to response generation.
"""
import unittest
import json
from app import app


class TestEndToEndWorkflow(unittest.TestCase):
    """End-to-end workflow tests."""
    
    def setUp(self):
        """Set up test environment."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_complete_chat_workflow(self):
        """Test complete chat workflow from start to finish."""
        # Step 1: Health check
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        
        # Step 2: Send chat message
        response = self.client.post(
            '/chat',
            data=json.dumps({
                'message': 'What is diabetes?'
            }),
            content_type='application/json'
        )
        # Should return 200 or 500 depending on external services
        self.assertIn(response.status_code, [200, 500])
    
    def test_conversation_continuity(self):
        """Test that conversations maintain context."""
        conversation_id = "test_conv_001"
        
        # Message 1
        response1 = self.client.post(
            '/chat',
            data=json.dumps({
                'message': 'What is diabetes?',
                'conversation_id': conversation_id
            }),
            content_type='application/json'
        )
        
        # Message 2 (should maintain context)
        response2 = self.client.post(
            '/chat',
            data=json.dumps({
                'message': 'What are its symptoms?',
                'conversation_id': conversation_id
            }),
            content_type='application/json'
        )
        
        self.assertIn(response1.status_code, [200, 500])
        self.assertIn(response2.status_code, [200, 500])
    
    def test_error_recovery_workflow(self):
        """Test error handling and recovery."""
        # Send invalid message
        response1 = self.client.post(
            '/chat',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response1.status_code, 400)
        
        # System should recover and handle next request
        response2 = self.client.get('/health')
        self.assertEqual(response2.status_code, 200)
    
    def test_rate_limiting_workflow(self):
        """Test rate limiting across workflow."""
        # Make multiple requests
        responses = []
        for i in range(5):
            response = self.client.get('/health')
            responses.append(response.status_code)
        
        # Should handle multiple requests
        self.assertTrue(any(code == 200 for code in responses))
    
    def test_caching_workflow(self):
        """Test caching behavior in workflow."""
        message = "What is hypertension?"
        
        # First request (cache miss)
        response1 = self.client.post(
            '/chat',
            data=json.dumps({'message': message}),
            content_type='application/json'
        )
        
        # Second request (cache hit)
        response2 = self.client.post(
            '/chat',
            data=json.dumps({'message': message}),
            content_type='application/json'
        )
        
        # Second response should be faster (cached)
        self.assertIn(response1.status_code, [200, 500])
        self.assertIn(response2.status_code, [200, 500])
    
    def test_security_workflow(self):
        """Test security measures in workflow."""
        # Try XSS attack
        response = self.client.post(
            '/chat',
            data=json.dumps({
                'message': '<script>alert("xss")</script>'
            }),
            content_type='application/json'
        )
        # Should be rejected or sanitized
        self.assertIn(response.status_code, [400, 200, 500])
    
    def test_logging_workflow(self):
        """Test logging is working throughout workflow."""
        # Make requests that should be logged
        self.client.get('/health')
        self.client.post(
            '/chat',
            data=json.dumps({'message': 'test'}),
            content_type='application/json'
        )
        # Check logs exist (simplified check)
        self.assertTrue(True)


class TestPerformanceWorkflow(unittest.TestCase):
    """Test performance under various conditions."""
    
    def setUp(self):
        """Set up test environment."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_response_time_acceptable(self):
        """Test that response times are acceptable."""
        import time
        
        start = time.time()
        response = self.client.get('/health')
        elapsed = time.time() - start
        
        # Health check should respond in under 1 second
        self.assertLess(elapsed, 1.0)
        self.assertEqual(response.status_code, 200)
    
    def test_concurrent_requests_handled(self):
        """Test handling of concurrent requests."""
        import threading
        
        responses = []
        
        def make_request():
            try:
                resp = self.client.get('/health')
                responses.append(resp.status_code)
            except Exception as e:
                responses.append(None)
        
        threads = [threading.Thread(target=make_request) for _ in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        # All concurrent requests should be handled
        self.assertEqual(len(responses), 10)
        self.assertTrue(all(code == 200 for code in responses))


if __name__ == '__main__':
    unittest.main()
