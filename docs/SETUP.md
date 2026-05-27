# Setup Guide

## Prerequisites

- Python 3.10+
- pip (Python package manager)
- Git
- API Keys for:
  - OpenAI (GPT-4)
  - Pinecone (Vector Database)

## Installation Steps

### 1. Clone Repository
```bash
git clone https://github.com/harshkushwaha7x/Medical-Chatbot.git
cd Medical-Chatbot
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```
PINECONE_API_KEY=your_pinecone_api_key
OPENAI_API_KEY=your_openai_api_key
FLASK_ENV=development
FLASK_DEBUG=True
```

### 5. Initialize Vector Store
```bash
python store_index.py
```

### 6. Run Application
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## Troubleshooting

### ImportError: No module named 'flask'
Solution: Ensure you have activated the virtual environment and installed requirements.

### API Key Errors
Solution: Verify `.env` file has correct credentials.

### Connection Refused
Solution: Check if Flask server is running on port 5000.

## Docker Deployment

```bash
docker build -t medical-chatbot .
docker run -p 5000:5000 --env-file .env medical-chatbot
```
