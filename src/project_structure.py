"""
Project structure and code organization guidelines.

This module documents the project structure and provides
guidelines for maintaining code organization.
"""
import logging

logger = logging.getLogger(__name__)


class ProjectStructure:
    """Documents project structure and organization."""
    
    STRUCTURE = {
        'src/': {
            'description': 'Core application source code',
            'modules': {
                'app.py': 'Main Flask application',
                'helper.py': 'PDF loading and processing utilities',
                'prompt.py': 'System prompts and prompt templates',
                'validation.py': 'Input validation and sanitization',
                'security.py': 'Security headers and CORS configuration',
                'error_handler.py': 'Error handling and recovery',
                'monitoring.py': 'Metrics collection and monitoring',
                'caching.py': 'Response caching system',
                'rate_limiter.py': 'Rate limiting middleware',
                'query_optimizer.py': 'Database query optimization',
                'performance.py': 'Performance benchmarking tools'
            }
        },
        'config/': {
            'description': 'Configuration files',
            'modules': {
                'settings.py': 'Application settings',
                'logging.py': 'Logging configuration',
                'database.py': 'Database and connection pooling',
                'security_config.py': 'Security configurations'
            }
        },
        'tests/': {
            'description': 'Test suite',
            'modules': {
                'test_helper.py': 'Tests for helper functions',
                'test_app.py': 'Tests for Flask app',
                'test_integration.py': 'Integration tests',
                'test_security.py': 'Security tests'
            }
        },
        'docs/': {
            'description': 'Documentation',
            'files': {
                'API.md': 'API documentation',
                'SETUP.md': 'Setup guide',
                'TROUBLESHOOTING.md': 'Troubleshooting guide',
                'SECURITY.md': 'Security best practices',
                'DEPLOYMENT.md': 'Deployment guide',
                'API_REFERENCE.md': 'Complete API reference'
            }
        },
        'templates/': {
            'description': 'HTML templates',
            'files': {
                'chat.html': 'Chat interface template'
            }
        },
        'static/': {
            'description': 'Static assets',
            'files': {
                'style.css': 'CSS styling'
            }
        },
        'data/': {
            'description': 'Data and resources',
            'files': {
                'Medical_book.pdf': 'Medical reference documents'
            }
        },
        'research/': {
            'description': 'Research and experimentation',
            'files': {
                'trials.ipynb': 'Jupyter notebook with experiments'
            }
        }
    }
    
    @staticmethod
    def get_structure() -> dict:
        """Get project structure."""
        return ProjectStructure.STRUCTURE
    
    @staticmethod
    def print_structure():
        """Print project structure."""
        structure = ProjectStructure.STRUCTURE
        
        lines = ["Medical Chatbot Project Structure", "=" * 50]
        
        for dir_name, dir_info in structure.items():
            lines.append(f"\n{dir_name}")
            lines.append(f"  Description: {dir_info.get('description', 'N/A')}")
            
            if 'modules' in dir_info:
                lines.append("  Modules:")
                for module, description in dir_info['modules'].items():
                    lines.append(f"    - {module}: {description}")
            
            if 'files' in dir_info:
                lines.append("  Files:")
                for file, description in dir_info['files'].items():
                    lines.append(f"    - {file}: {description}")
        
        report = "\n".join(lines)
        logger.info(report)
        return report


class CodingStandards:
    """Defines coding standards for the project."""
    
    STANDARDS = {
        'naming': {
            'modules': 'snake_case (e.g., error_handler.py)',
            'classes': 'PascalCase (e.g., ChatbotError)',
            'functions': 'snake_case (e.g., validate_message)',
            'constants': 'UPPER_SNAKE_CASE (e.g., MAX_FILE_SIZE)'
        },
        'documentation': {
            'modules': 'Module docstring at top of file',
            'classes': 'Class docstring describing purpose',
            'functions': 'Function docstring with Args, Returns, Raises',
            'comments': 'Inline comments for complex logic'
        },
        'code_style': {
            'line_length': 'Maximum 100 characters',
            'imports': 'Group by stdlib, third-party, local',
            'formatting': 'Follow PEP 8 style guide',
            'type_hints': 'Use type hints for better IDE support'
        },
        'error_handling': {
            'approach': 'Use custom exception classes',
            'logging': 'Log all errors with context',
            'recovery': 'Implement retry logic for transient errors'
        }
    }
    
    @staticmethod
    def get_standards() -> dict:
        """Get coding standards."""
        return CodingStandards.STANDARDS


def organize_imports(f):
    """Decorator to document import organization."""
    import inspect
    source = inspect.getsource(f)
    logger.debug(f"Function {f.__name__} uses imports:\n{source[:200]}")
    return f


# Project initialization
logger.info("Project structure and organization guidelines loaded")
