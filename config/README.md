# Configuration Management

This module provides centralized configuration management for the Medical Chatbot application.

## Configuration Files

- `development.py` - Development environment settings
- `production.py` - Production environment settings
- `testing.py` - Testing environment settings

## Usage

```python
from config.settings import Config

# Load environment-specific configuration
config = Config.from_env()

# Access configuration values
api_key = config.OPENAI_API_KEY
debug_mode = config.DEBUG
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| OPENAI_API_KEY | OpenAI API key | Yes |
| PINECONE_API_KEY | Pinecone API key | Yes |
| FLASK_ENV | Environment (development/production) | No |
| FLASK_DEBUG | Debug mode (True/False) | No |
| LOG_LEVEL | Logging level (DEBUG/INFO/WARNING) | No |

## Configuration Override

Override default settings via environment variables:

```bash
export FLASK_ENV=production
export LOG_LEVEL=WARNING
```
