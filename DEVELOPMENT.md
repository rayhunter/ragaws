# Development Guide

## Local Development Setup

### Backend

1. **Create virtual environment**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. **Run development server**:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

1. **Install dependencies**:
```bash
cd frontend
npm install
```

2. **Configure environment**:
```bash
cp .env.example .env
# Edit .env: VITE_API_URL=http://localhost:8000
```

3. **Run development server**:
```bash
npm run dev
```

### Using Docker Compose

For a complete local stack:

```bash
docker-compose up --build
```

Backend: http://localhost:8000
Frontend: http://localhost:80

## Testing

### Backend Tests

```bash
cd backend
pytest tests/
```

### Frontend Tests

```bash
cd frontend
npm test
```

## API Testing

### Upload Document

```bash
curl -X POST http://localhost:8000/api/v1/ingestion/upload \
  -F "file=@example.pdf"
```

### Query (Retrieval)

```bash
curl -X POST http://localhost:8000/api/v1/retrieval/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic?", "top_k": 5}'
```

### Generate (Generation)

```bash
curl -X POST http://localhost:8000/api/v1/generation/generate \
  -H "Content-Type: application/json" \
  -d '{
    "context": "<context>\nSome context here\n</context>",
    "question": "What is this about?",
    "max_tokens": 500
  }'
```

## Code Structure

### Backend

- `app/main.py` - FastAPI application entry point
- `app/core/` - Core modules (txtai client, bedrock client, config)
- `app/routers/` - API route handlers (ingestion, retrieval, generation)

### Frontend

- `src/App.jsx` - Main application component
- `src/components/` - React components (UploadSection, QuerySection, ResultsSection)

## Best Practices

1. **Environment Variables**: Never commit `.env` files
2. **Error Handling**: Always handle errors gracefully
3. **Logging**: Use structured logging for production
4. **Testing**: Write tests for critical paths
5. **Documentation**: Keep API docs updated

## Debugging

### Backend

- Check logs: `tail -f logs/app.log`
- Use FastAPI docs: http://localhost:8000/docs
- Enable debug mode: Set `DEBUG=True` in `.env`

### Frontend

- Use React DevTools
- Check browser console for errors
- Use Network tab to inspect API calls

