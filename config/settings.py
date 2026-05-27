"""
Configuration settings for Medical Chatbot application.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration class."""
    
    DEBUG = False
    TESTING = False
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
    
    # Application Settings
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    @classmethod
    def from_env(cls):
        """Load configuration from environment."""
        env = os.getenv('FLASK_ENV', 'development')
        if env == 'production':
            return ProductionConfig()
        elif env == 'testing':
            return TestingConfig()
        return DevelopmentConfig()


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
