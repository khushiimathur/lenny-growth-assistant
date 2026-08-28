# The Lenny Growth Assistant — Architecture

## 1. System Overview

```text
                    ┌──────────────────────┐
                    │      React UI        │
                    │  Chat + Artifact UI  │
                    └──────────┬───────────┘
                               │ HTTP
                               ▼
                    ┌──────────────────────┐
                    │      FastAPI         │
                    │  Sessions / Chat API │
                    └───────┬───────┬──────┘
                            │       │
                            │       ▼
                            │  PostgreSQL
                            │  sessions/messages
                            │
                            ▼
                    ┌──────────────────────┐
                    │      RAG Service     │
                    └──────────┬───────────┘
                               │
                     ┌─────────┴─────────┐
                     ▼                   ▼
                Retriever            Ollama
                     │                   │
                     ▼                   ▼
                  Chroma          Local LLM
                     │
                     ▼
              Lenny transcript
                embeddings
```

## 2. Component Boundaries

### FastAPI

Responsible for:

- HTTP API
- request validation
- session validation
- database access
- invoking RAG
- returning structured responses

### Knowledge Layer

Responsible for:

- transcript loading
- cleaning
- document representation
- chunking
- embeddings
- vector storage
- retrieval
- RAG prompt construction

### LLM Layer

`OllamaClient` isolates local model communication from the rest of the application.

### Database Layer

PostgreSQL stores:

- session ID
- user ID
- session creation time
- message ID
- role
- message content
- message creation time

## 3. Database Schema

### chat_sessions

```text
id          VARCHAR(36) PRIMARY KEY
user_id     VARCHAR(100)
created_at  TIMESTAMP NOT NULL
```

### messages

```text
id          VARCHAR(36) PRIMARY KEY
session_id  VARCHAR(36) NOT NULL
role        VARCHAR(20) NOT NULL
content     TEXT NOT NULL
created_at  TIMESTAMP NOT NULL
```

`messages.session_id` references `chat_sessions.id`.

## 4. API

### Health

```http
GET /health
```

Returns API health information.

### Create Session

```http
POST /api/sessions
```

Example:

```json
{
  "user_id": "demo-user"
}
```

### Chat

```http
POST /chat
```

Example:

```json
{
  "session_id": "<session-id>",
  "message": "How do I improve product retention?"
}
```

### Message History

```http
GET /api/sessions/{session_id}/messages
```

Returns persisted messages for the session.

## 5. Ingestion Flow

```text
Lenny transcript repository
        ↓
episodes/<episode>/transcript.md
        ↓
loader.py
        ↓
cleaner.py
        ↓
chunker.py
        ↓
embeddings.py
        ↓
vector_store.py
        ↓
ChromaDB
```

The ingestion process successfully processes the available transcript collection and stores source metadata such as guest, episode title, timestamps, and transcript text.

## 6. Retrieval Flow

```text
User question
      ↓
Embedding
      ↓
Chroma similarity search
      ↓
Top relevant transcript chunks
      ↓
RAG prompt
      ↓
Ollama
      ↓
Grounded answer + source metadata
```

Conversation history is included so follow-up questions can be interpreted in session context.

## 7. Agent/Skill Direction

The project contains a lightweight intent/skill boundary for chat, Markdown, HTML, and Ship 30-style content generation.

The intended routing model is:

```text
User request
    ↓
Intent / skill router
    ├── chat → RAG
    ├── markdown → RAG + artifact generation
    ├── html → RAG + HTML generation
    └── ship30 → RAG + Ship 30 writing skill
```

A full Anthropic Claude Agent SDK/Pi Coding Agent integration was not completed in the submitted MVP. This is a known gap against the assignment requirement.

## 8. Model Configuration

The current submitted demo uses Ollama locally.

```text
Application
    ↓
OllamaClient
    ↓
localhost:11434
    ↓
local model
```

A future provider abstraction can support:

```text
LLM_PROVIDER=ollama
LLM_PROVIDER=anthropic
LLM_PROVIDER=openai
```

without changing the RAG interface.

## 9. Artifact Security

Generated HTML is considered untrusted.

The frontend does not use `dangerouslySetInnerHTML` for generated HTML. Instead it renders HTML using:

```text
iframe
  └── sandbox=""
```

The generated HTML is also instructed not to use JavaScript or external resources.

This reduces the ability of generated content to access the parent React application.

## 10. Deployment Topology

The current development topology is:

```text
Browser
  │
  ├── React: localhost:5173
  │
  └── FastAPI: localhost:8000
          │
          ├── PostgreSQL: Docker container
          ├── ChromaDB: local vector store
          └── Ollama: localhost:11434
```

The repository documents the services required to reproduce the local setup.

## 11. Trade-offs

### Local Ollama

Pros:
- No inference API cost
- Easy local demonstration
- Keeps transcript prompts/data local

Cons:
- Higher latency
- Hardware-dependent model quality

### ChromaDB

Pros:
- Simple local vector database
- Easy Python integration

Cons:
- Less operationally mature than a managed vector service for production.

### PostgreSQL

Used for durable conversational state rather than storing chat history only in browser memory.

### Simple React state

The MVP uses React hooks rather than introducing a state-management framework because the application has a small state surface.
