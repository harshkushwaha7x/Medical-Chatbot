"""
Unit tests for Medical Chatbot helper functions.
"""
import unittest
from src.helper import download_hugging_face_embeddings


class TestEmbeddings(unittest.TestCase):
    """Test embedding functionality."""
    
    def test_embeddings_download(self):
        """Test that embeddings can be downloaded."""
        try:
            embeddings = download_hugging_face_embeddings()
            self.assertIsNotNone(embeddings)
        except Exception as e:
            self.fail(f"Failed to download embeddings: {e}")
    
    def test_embeddings_dimension(self):
        """Test embedding dimensions."""
        embeddings = download_hugging_face_embeddings()
        # HuggingFace embeddings should have proper dimensions
        self.assertGreater(embeddings.client.get_sentence_embedding_dimension(), 0)


class TestConfiguration(unittest.TestCase):
    """Test configuration loading."""
    
    def test_config_from_env(self):
        """Test that configuration loads from environment."""
        from config.settings import Config
        config = Config.from_env()
        self.assertIsNotNone(config)


if __name__ == '__main__':
    unittest.main()
