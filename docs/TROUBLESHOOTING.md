# Troubleshooting Guide

## Common Issues and Solutions

### 1. ImportError: No module named 'langchain'

**Problem:** Python can't find the langchain library.

**Solutions:**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`
- Check Python version is 3.10+

### 2. PINECONE_API_KEY not found

**Problem:** Application fails to authenticate with Pinecone.

**Solutions:**
- Verify `.env` file exists in project root
- Check `.env` file has `PINECONE_API_KEY=your_key`
- Never commit `.env` file to GitHub
- Use `.env.example` as template

### 3. Connection timeout to Pinecone

**Problem:** Application can't connect to vector database.

**Solutions:**
- Check internet connection
- Verify API key is valid
- Check Pinecone service status
- Run `python store_index.py` to reinitialize

### 4. Flask port already in use

**Problem:** Port 5000 is already occupied.

**Solutions:**
- Change port: `python app.py --port 5001`
- Or kill process using port 5000
- Windows: `netstat -ano | findstr :5000`
- macOS/Linux: `lsof -i :5000`

### 5. Out of memory error

**Problem:** Application crashes with memory error.

**Solutions:**
- Reduce batch size in processing
- Check available system RAM
- Monitor resource usage with Task Manager

### 6. PDF loading fails

**Problem:** Can't load medical PDFs.

**Solutions:**
- Ensure PDFs are valid (not corrupted)
- Check file permissions
- Verify PDF path is correct
- Use `pypdf` to validate PDF structure

## Logging

Enable detailed logging to diagnose issues:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check logs in:
- Console output
- `logs/` directory (if configured)
