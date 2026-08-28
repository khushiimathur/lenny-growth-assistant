# The Lenny Growth Assistant — PRD

## 1. Product Overview

The Lenny Growth Assistant is a full-stack AI assistant for product managers and growth teams. It uses Lenny's Podcast transcripts as a knowledge base to answer product and growth questions with source attribution and conversation context.

The assignment asks for a reliable internal assistant that turns Lenny's content into grounded answers and reusable content/artifacts.

## 2. Discovery Brief

### User

The primary user is a product manager, product leader, founder, or growth practitioner who wants practical product advice without manually searching hundreds of podcast transcripts.

### Problem

Relevant advice is distributed across a large transcript collection. Finding the right episode, locating the relevant discussion, and synthesizing perspectives is time-consuming.

### Job to Be Done

"When I have a product or growth question, I want to ask it conversationally and quickly receive a useful answer grounded in Lenny's Podcast transcripts, with enough source information to investigate further."

### Pain Removed

- Manual transcript searching
- Reading multiple long transcripts
- Losing context between follow-up questions
- Separately synthesizing advice from multiple guests

## 3. Success Metrics

### Primary

- A user can ask a product/growth question and receive a grounded answer with relevant transcript sources in one interaction.

### Operational

- Transcript ingestion completes successfully for the available episode collection.
- API health endpoint responds successfully.
- Critical backend tests pass.
- A multi-turn conversation preserves the selected session context.

## 4. Assumptions

- Lenny's Podcast transcripts are the authoritative knowledge source for the assistant.
- Users prefer grounded answers over generic LLM knowledge.
- Local Ollama is acceptable for the submitted demo.
- PostgreSQL is used for durable conversation/session state.
- ChromaDB is used as the local vector store.
- The current MVP prioritizes correctness and a simple usable interface over advanced visual polish.
- The frontend uses a demo user rather than a full authentication system.

## 5. Scope

### Included

- Transcript loading from Markdown files
- Transcript cleaning and chunking
- Embedding generation
- ChromaDB vector retrieval
- RAG-based conversational answers
- Source metadata in responses
- PostgreSQL session and message persistence
- Follow-up conversation context
- FastAPI API
- React chat interface
- Basic artifact response/viewer work
- Local Ollama model integration
- CORS configuration for local frontend/backend development

### Intentionally Excluded / Simplified

- Full authentication and authorization
- Multi-user account management
- Production-grade cloud deployment
- Advanced reranking
- Streaming token responses
- Complex agent orchestration
- Advanced UI animations

These were deprioritized to deliver a working end-to-end MVP within the assignment timeline.

## 6. User Flows

### New Chat

1. User opens the application.
2. Frontend creates a new session through `POST /api/sessions`.
3. Backend stores the session in PostgreSQL.
4. Frontend receives the `session_id`.

### Normal Question

1. User submits a question.
2. Backend validates the session.
3. Previous messages for that session are loaded.
4. Retriever finds relevant transcript chunks.
5. RAG prompt combines the question, history, and retrieved excerpts.
6. Ollama generates the answer.
7. User and assistant messages are persisted.
8. Answer and source metadata are returned to the frontend.

### Follow-up

A subsequent question uses the same `session_id`, allowing the backend to include recent conversation history in the RAG prompt.

## 7. Acceptance Criteria

- User can create a new chat.
- Each session has independent context.
- User can send product/growth questions.
- Answers are generated using retrieved transcript evidence.
- Responses expose source metadata.
- Follow-up questions use conversation history.
- Messages persist in PostgreSQL.
- The application runs locally with documented setup steps.
- The frontend provides a simple usable chat experience.

## 8. Risks and Trade-offs

### Hallucination

The system may generate claims not supported by retrieved evidence. Mitigation: retrieval-grounded prompts explicitly instruct the model not to invent claims.

### Retrieval Quality

Poor chunking or retrieval can surface irrelevant excerpts. Mitigation: transcript-specific cleaning, timestamp-aware chunking, embeddings, and source metadata.

### Local Model Quality

Ollama provides a convenient local model but may be slower or less capable than a hosted model.

### Latency

Embedding model loading and local LLM inference can make requests slow. The MVP favors local reproducibility over minimum latency.

### Artifact Security

Generated HTML must be treated as untrusted. The frontend uses a sandboxed iframe approach rather than directly injecting generated HTML into the React DOM.

### Cost

Using Ollama locally avoids cloud inference costs for the submitted demo.

## 9. Implementation Plan

1. Build transcript ingestion pipeline.
2. Build semantic retrieval.
3. Add RAG answer generation.
4. Add PostgreSQL sessions/messages.
5. Add FastAPI chat APIs.
6. Add conversation history.
7. Build basic React UI.
8. Add artifact handling/viewer.
9. Add tests and operational documentation.
10. Validate the end-to-end demo.

## 10. Current MVP Status

The core conversational RAG application is implemented and working locally. Some assignment requirements, including a full cloud-provider toggle and formal coding-agent integration, remain outside the current MVP scope and should be clearly documented rather than represented as complete.
