# Lenny Growth Assistant

A full-stack conversational RAG assistant grounded in Lenny's Podcast transcripts.

## Features

- 303 Lenny transcript sources ingested
- Markdown transcript loading
- Transcript cleaning and timestamp-aware chunking
- Sentence-transformer embeddings
- ChromaDB semantic retrieval
- RAG-based answers
- Source metadata in responses
- PostgreSQL session/message persistence
- Multi-turn conversation context
- FastAPI backend
- React frontend
- Local Ollama inference
- Basic Markdown/HTML artifact handling

## Architecture

```text
React
  ↓
FastAPI
  ↓
RAG Service
  ├── Retriever → ChromaDB
  ├── Prompt Builder
  └── Ollama Client
         ↓
      Local LLM

PostgreSQL
  ├── chat_sessions
  └── messages
```

## Prerequisites

- Python 3.10+
- Node.js/npm
- Docker
- Ollama
- Lenny transcript repository/data
- PostgreSQL running locally or through Docker

## Backend Setup

```bash
cd backend

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## PostgreSQL

Start the PostgreSQL container according to the repository's Docker configuration.

Example:

```bash
docker compose up -d
```

Verify:

```bash
docker ps
```

## Ollama

Install Ollama and pull the local model used by the application.

Example:

```bash
ollama pull llama3.2
```

Make sure Ollama is running before sending chat requests.

## Transcript Ingestion

The transcript data follows the Lenny repository structure:

```text
data/
└── episodes/
    ├── episode-name/
    │   └── transcript.md
    └── ...
```

Run ingestion from `backend`:

```bash
python -m scripts.ingest
```

The ingestion pipeline loads transcripts, cleans them, chunks them, generates embeddings, and stores them in ChromaDB with source metadata.

## Start Backend

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

Backend:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

## Start Frontend

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

## Application Flow

1. Frontend creates a session.
2. User sends a question.
3. FastAPI validates the session.
4. Recent conversation history is loaded from PostgreSQL.
5. Relevant transcript chunks are retrieved from ChromaDB.
6. The RAG prompt is sent to Ollama.
7. The answer and source metadata are returned.
8. User and assistant messages are saved in PostgreSQL.

## Testing

From `backend`:

```bash
pytest -v
```

## Troubleshooting

### Send button disabled

Check that the frontend successfully created a session and that the backend allows CORS from:

```text
http://localhost:5173
```

### CORS / OPTIONS 405

Make sure FastAPI has `CORSMiddleware` configured before starting the server.

### Ollama timeout

Confirm Ollama is running and the configured model is available:

```bash
ollama list
```

Local model inference can take longer on CPU-only systems.

### Chroma retrieval is empty

Run the ingestion script again and verify that the transcript collection has been populated.

### PostgreSQL connection failure

Check:

```bash
docker ps
```

and verify the database URL/environment configuration.

## Environment Variables

Do not commit secrets.

Recommended variables include:

```text
DATABASE_URL=
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
LLM_PROVIDER=ollama
ANTHROPIC_API_KEY=
```

## Known Limitations

This submission prioritizes a working local RAG MVP. Full cloud-provider switching and formal Claude Agent SDK/Pi Coding Agent integration were not completed in the available implementation time.

The local Ollama path is the demonstrated model path.

## Future Improvements

- Formal Claude Agent SDK/Pi Coding Agent integration
- Cloud/local model toggle in UI
- Stronger intent routing
- Complete Ship 30 skill
- More robust Markdown/HTML artifact generation
- Streaming responses
- Authentication
- Production deployment
- Better observability and structured error responses
