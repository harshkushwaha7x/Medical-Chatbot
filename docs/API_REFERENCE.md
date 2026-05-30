# API Reference Documentation

## Base URL
```
https://api.medical-chatbot.com/api/v1
```

## Authentication

All requests require an API key in the header:

```bash
X-API-Key: your_api_key_here
```

---

## Endpoints

### 1. Chat Endpoint

**POST** `/chat`

Send a message to the medical chatbot and receive a response.

#### Request

```bash
curl -X POST https://api.medical-chatbot.com/api/v1/chat \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d {
    "message": "What are the symptoms of diabetes?",
    "conversation_id": "optional_conversation_id"
  }
```

#### Request Body

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| message | string | Yes | User query (max 5000 characters) |
| conversation_id | string | No | ID to group related messages |

#### Response (200 OK)

```json
{
  "response": "Diabetes symptoms include increased thirst, frequent urination, fatigue...",
  "sources": [
    "medical_book.pdf - page 45",
    "endocrinology_guide.pdf - page 12"
  ],
  "conversation_id": "conv_123456",
  "confidence": 0.95,
  "timestamp": "2026-05-30T10:30:00Z"
}
```

#### Error Responses

**400 Bad Request**
```json
{
  "error": "Message cannot be empty",
  "type": "ValidationError"
}
```

**401 Unauthorized**
```json
{
  "error": "Invalid API key",
  "type": "AuthenticationError"
}
```

**429 Too Many Requests**
```json
{
  "error": "Rate limit exceeded",
  "type": "RateLimitError",
  "details": {
    "retry_after": 60
  }
}
```

**500 Internal Server Error**
```json
{
  "error": "An unexpected error occurred",
  "type": "InternalServerError"
}
```

---

### 2. Health Check Endpoint

**GET** `/health`

Check the health status of the API.

#### Request

```bash
curl https://api.medical-chatbot.com/api/v1/health
```

#### Response (200 OK)

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime": "48 hours",
  "database": "connected",
  "llm_service": "connected",
  "timestamp": "2026-05-30T10:30:00Z"
}
```

---

### 3. Metrics Endpoint

**GET** `/metrics`

Get application metrics (requires admin key).

#### Request

```bash
curl https://api.medical-chatbot.com/api/v1/metrics \
  -H "X-Admin-Key: admin_key"
```

#### Response (200 OK)

```json
{
  "total_requests": 15000,
  "total_errors": 45,
  "error_rate": 0.3,
  "avg_response_time": "0.35s",
  "cache_hits": 8500,
  "cache_hit_rate": "85%",
  "uptime": "48 hours"
}
```

---

### 4. Conversation History Endpoint

**GET** `/conversations/{conversation_id}`

Retrieve conversation history.

#### Request

```bash
curl https://api.medical-chatbot.com/api/v1/conversations/conv_123456 \
  -H "X-API-Key: your_api_key"
```

#### Response (200 OK)

```json
{
  "conversation_id": "conv_123456",
  "created_at": "2026-05-30T08:00:00Z",
  "messages": [
    {
      "role": "user",
      "content": "What is diabetes?",
      "timestamp": "2026-05-30T08:00:00Z"
    },
    {
      "role": "assistant",
      "content": "Diabetes is a metabolic disorder...",
      "timestamp": "2026-05-30T08:00:05Z"
    }
  ]
}
```

---

## Rate Limiting

- **Limit**: 100 requests per hour per API key
- **Headers**: Include `X-RateLimit-Remaining` and `X-RateLimit-Reset`
- **Exceeding**: Returns 429 status code

---

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Invalid API key |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |
| 503 | Service Unavailable - External API error |

---

## Best Practices

1. **Use Conversation IDs**: Group related messages to maintain context
2. **Handle Rate Limits**: Implement exponential backoff
3. **Cache Results**: Store frequently asked questions
4. **Monitor API**: Track usage and errors
5. **Use Appropriate Timeouts**: Set 30-second timeout for requests

---

## Code Examples

### Python

```python
import requests

url = "https://api.medical-chatbot.com/api/v1/chat"
headers = {
    "X-API-Key": "your_api_key",
    "Content-Type": "application/json"
}
data = {
    "message": "What is hypertension?",
    "conversation_id": "conv_123"
}

response = requests.post(url, json=data, headers=headers)
result = response.json()
print(result['response'])
```

### JavaScript

```javascript
const url = "https://api.medical-chatbot.com/api/v1/chat";
const options = {
  method: "POST",
  headers: {
    "X-API-Key": "your_api_key",
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    message: "What is hypertension?",
    conversation_id: "conv_123"
  })
};

const response = await fetch(url, options);
const data = await response.json();
console.log(data.response);
```

### cURL

```bash
curl -X POST https://api.medical-chatbot.com/api/v1/chat \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{"message":"What is hypertension?","conversation_id":"conv_123"}'
```

---

## Support

- Email: support@medical-chatbot.com
- Documentation: https://docs.medical-chatbot.com
- GitHub: https://github.com/harshkushwaha7x/Medical-Chatbot
