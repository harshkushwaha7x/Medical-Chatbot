# Security Best Practices Guide

## Overview

This guide outlines security best practices for the Medical Chatbot application.

## 1. Input Validation & Sanitization

### Validate All Inputs

```python
from src.validation import InputValidator, validate_request_data

# Validate incoming requests
is_valid, error = validate_request_data(request.json)
if not is_valid:
    return jsonify({'error': error}), 400
```

### Common Injection Attacks

- **SQL Injection**: Use parameterized queries, avoid string concatenation
- **XSS (Cross-Site Scripting)**: Sanitize HTML, use Content Security Policy
- **Command Injection**: Never execute user input as commands

### Validation Rules

- Maximum message length: 5000 characters
- Reject suspicious patterns (script tags, SQL keywords)
- Validate email addresses and URLs
- Check file types and sizes

## 2. Authentication & Authorization

### API Key Security

```python
# Never commit API keys
# Always use environment variables
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
```

### Secret Management

- Use `.env` files (never commit)
- Rotate API keys regularly
- Use different keys for development/production
- Store secrets in secure vaults (AWS Secrets Manager, HashiCorp Vault)

## 3. Data Protection

### Encryption

```python
# Encrypt sensitive data at rest
# Use HTTPS for data in transit
# Enable TLS 1.2 or higher
```

### Data Retention

- Define data retention policies
- Implement data deletion after retention period
- Regular backups with encryption
- Test recovery procedures

## 4. CORS Protection

```python
# Configure CORS to allow specific origins only
ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'https://yourdomain.com'
]

CORS(app, resources={
    r"/api/*": {"origins": ALLOWED_ORIGINS}
})
```

## 5. Security Headers

### Essential Headers

| Header | Value | Purpose |
|--------|-------|---------|
| X-Frame-Options | DENY | Prevent clickjacking |
| X-Content-Type-Options | nosniff | Prevent MIME sniffing |
| Content-Security-Policy | default-src 'self' | XSS protection |
| Strict-Transport-Security | max-age=31536000 | Force HTTPS |

## 6. Rate Limiting

```python
from src.rate_limiter import rate_limit

@app.route('/chat', methods=['POST'])
@rate_limit
def chat():
    # Endpoint protected by rate limiting
    pass
```

### Rate Limit Settings

- 100 requests per hour per IP
- Adjust based on requirements
- Return 429 status for exceeded limits

## 7. Error Handling

### Secure Error Messages

```python
# ❌ Don't expose sensitive information
return jsonify({'error': 'Database connection failed: ' + str(e)}), 500

# ✅ Generic error messages
return jsonify({'error': 'An error occurred. Please try again.'}), 500
```

## 8. Logging & Monitoring

### Log Sensitive Events

```python
import logging

logger = logging.getLogger(__name__)

# Log security events
logger.warning(f"Failed login attempt from {ip_address}")
logger.info(f"Rate limit exceeded for {client_id}")
logger.error(f"Invalid API key attempt")
```

### What NOT to Log

- Passwords or API keys
- Personal information (PII)
- Credit card numbers
- Private encryption keys

## 9. Dependency Management

### Keep Dependencies Updated

```bash
# Check for vulnerabilities
pip install safety
safety check

# Update packages
pip install --upgrade package_name
```

### Vulnerable Dependencies

- Monitor security advisories
- Use tools like `snyk` or `safety`
- Automate dependency updates (Dependabot)

## 10. API Security

### Authentication

```python
# Implement API key authentication
def verify_api_key(api_key):
    valid_keys = os.environ.get('VALID_API_KEYS', '').split(',')
    return api_key in valid_keys

@app.before_request
def check_api_key():
    api_key = request.headers.get('X-API-Key')
    if not api_key or not verify_api_key(api_key):
        return jsonify({'error': 'Invalid API key'}), 401
```

### Rate Limiting

```python
# Apply rate limiting to all endpoints
@app.route('/api/chat', methods=['POST'])
@rate_limit
def chat():
    pass
```

## 11. SSL/TLS Configuration

### HTTPS Requirements

- Always use HTTPS in production
- Use certificates from trusted CAs
- Enable HSTS (HTTP Strict-Transport-Security)
- Minimum TLS 1.2

### Certificate Management

```bash
# Using Let's Encrypt
certbot certonly --standalone -d yourdomain.com
```

## 12. Regular Security Audits

### Security Checklist

- [ ] All inputs validated
- [ ] No hardcoded secrets
- [ ] HTTPS enabled
- [ ] Security headers configured
- [ ] Rate limiting active
- [ ] Error handling secure
- [ ] Dependencies up to date
- [ ] Logging configured
- [ ] Database encrypted
- [ ] Access controls implemented

### Tools

- **OWASP ZAP**: Vulnerability scanner
- **Bandit**: Python security issue scanner
- **Safety**: Dependency vulnerability checker
- **SonarQube**: Code quality and security

## 13. Incident Response

### Security Incident Procedure

1. **Detect**: Monitor logs and alerts
2. **Contain**: Isolate affected systems
3. **Investigate**: Analyze root cause
4. **Eradicate**: Remove threat
5. **Recover**: Restore systems
6. **Review**: Improve processes

### Contact Information

- Security team: security@yourdomain.com
- Incident hotline: +1-XXX-XXX-XXXX
- Report vulnerabilities: security@yourdomain.com

## 14. Compliance

### Standards

- OWASP Top 10
- HIPAA (for healthcare data)
- GDPR (for EU users)
- PCI DSS (if processing payments)

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security](https://flask.palletsprojects.com/en/security/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
