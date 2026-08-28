# The Lenny Growth Assistant — Design

## 1. Design Goals

The interface is designed around three principles:

1. **Ask first** — the user should immediately understand where to ask a question.
2. **Show evidence** — sources should be visible with assistant answers.
3. **Keep generated work nearby** — artifacts can be viewed beside the conversation.

## 2. Information Architecture

```text
Application
├── Sidebar
│   ├── Application name
│   └── New Chat
│
├── Chat Area
│   ├── Header
│   ├── Conversation
│   └── Message input
│
└── Artifact Area
    ├── Artifact title
    ├── Generated Markdown/HTML
    └── Close/Open controls
```

## 3. Chat Interaction

### Empty State

The empty state explains what the assistant can answer and provides example questions such as:

- How do I know if my product has product-market fit?
- How can I improve product retention?
- What makes a great product manager?

### User Message

User messages are visually separated from assistant messages.

### Assistant Message

Each assistant message contains:

- Answer text
- Optional source list
- Guest/episode metadata
- Timestamp where available

### Loading State

While the local model is generating a response, the interface displays a simple "Thinking..." state and disables the Send button.

### Error State

If an API request fails, the interface displays a concise retry-oriented error message.

## 4. Artifact Viewer

The artifact viewer occupies a separate panel beside the chat when an artifact is available.

Markdown artifacts are displayed as document content.

HTML artifacts are rendered in an iframe with sandboxing rather than directly inserted into the React DOM.

## 5. Responsive Behavior

The MVP targets desktop usage because the assignment is primarily evaluated as a developer/product workflow. The layout uses flexible sizing so the chat remains usable when the artifact panel is present.

## 6. Accessibility

- Buttons have descriptive labels.
- Text input has a clear placeholder.
- Keyboard Enter submits a message; Shift+Enter allows a new line.
- The HTML iframe has a title.
- Contrast and spacing are kept simple and readable.
- Interactive controls use native buttons where possible.

## 7. Design Decisions

### Why a simple interface?

The primary value is grounded product knowledge, not visual complexity. A simple UI reduces implementation risk and keeps attention on answers, sources, and artifacts.

### Why a separate artifact panel?

The assignment explicitly asks for artifacts to render beside the chat. A separate panel lets users continue reading the conversation while inspecting generated work.

### Why a sandboxed iframe?

Generated HTML is untrusted. Rendering it in a sandboxed iframe limits its ability to interact with the parent application.
