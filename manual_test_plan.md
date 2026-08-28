# Manual UI Test Plan

## 1. Application Startup

**Steps**
1. Start PostgreSQL.
2. Start Ollama.
3. Start FastAPI.
4. Start React.
5. Open `http://localhost:5173`.

**Expected**
- Application loads.
- Chat interface is visible.
- A session is created automatically.

## 2. Create New Chat

**Steps**
1. Click `+ New Chat`.
2. Send a question.

**Expected**
- New session is created.
- Previous conversation is not shown in the new chat.
- New message is stored under the new session.

## 3. Normal RAG Question

**Input**

```text
How do I improve product retention?
```

**Expected**
- Assistant returns an answer.
- Answer is based on retrieved transcript material.
- Relevant guest/episode source information is displayed.

## 4. Follow-up Context

**Input 1**

```text
How do I improve product retention?
```

**Input 2**

```text
What metrics should I track?
```

**Input 3**

```text
Which one would you prioritize?
```

**Expected**
- Each response uses the same session.
- Follow-up questions retain context.

## 5. Persistence

**Steps**
1. Send several messages.
2. Query PostgreSQL.
3. Call the message history endpoint.

**Expected**
- User and assistant messages are persisted.
- Messages have session IDs and timestamps.

## 6. Artifact

**Input**

```text
Create a Markdown document explaining how to improve product retention.
```

**Expected**
- Backend returns an artifact when the artifact route is detected.
- Frontend displays it in the artifact area.

## 7. Error Handling

**Steps**
1. Stop Ollama.
2. Send a chat message.

**Expected**
- The UI does not crash.
- The failure is communicated to the user/logs.

## 8. API Validation

**Steps**
1. Send `/chat` with an invalid session ID.
2. Send an empty message.

**Expected**
- Invalid session returns an appropriate 4xx response.
- Empty message is rejected by request validation.

## 9. Responsive/Usability Check

Verify:
- Chat messages can scroll independently.
- Input remains accessible.
- Artifact panel does not cover the entire application.
- Buttons have clear labels.
