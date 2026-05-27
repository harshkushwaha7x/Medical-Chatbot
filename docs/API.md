# API Documentation

## Medical Chatbot API Endpoints

### POST /chat
Send a message to the chatbot and receive a response.

**Request:**
```json
{
  "message": "What are the symptoms of diabetes?"
}
```

**Response:**
```json
{
  "response": "Symptoms of diabetes include...",
  "sources": ["source1.pdf", "source2.pdf"]
}
```

### GET /health
Check the health status of the chatbot service.

**Response:**
```json
{
  "status": "healthy",
  "model": "gpt-4",
  "embeddings": "sentence-transformers"
}
```

### POST /clear-history
Clear conversation history.

**Response:**
```json
{
  "message": "Chat history cleared",
  "success": true
}
```

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200 OK` - Successful request
- `400 Bad Request` - Invalid input
- `500 Internal Server Error` - Server error

## Rate Limiting

API is rate limited to 100 requests per hour per IP address.
