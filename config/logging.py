"""
Logging configuration for Medical Chatbot.
"""
import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(app, log_level='INFO'):
    """Configure application logging."""
    
    # Create logs directory if not exists
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        'logs/medical_chatbot.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    console_handler.setLevel(getattr(logging, log_level))
    
    # Add handlers to app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(getattr(logging, log_level))
    
    return app.logger
