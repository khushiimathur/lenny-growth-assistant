import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://localhost:8000";

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  
  const [artifact, setArtifact] = useState(null);
  const [showArtifact, setShowArtifact] = useState(true);
  async function createSession() {
    const response = await fetch(`${API_URL}/api/sessions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: "demo-user",
      }),
    });

    if (!response.ok) {
      throw new Error("Failed to create session");
    }

    const data = await response.json();

    setSessionId(data.id);
    setMessages([]);
    setArtifact(null);
    setShowArtifact(false);
  }

  async function sendMessage() {
    if (!input.trim() || !sessionId || loading) {
      return;
    }

    const userMessage = input.trim();

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    setInput("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: sessionId,
          message: userMessage,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to get response");
      }

      const data = await response.json();
      setArtifact(data.artifact || null);
      if (data.artifact) {
  setShowArtifact(true);
}
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
          sources: data.sources || [],
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Sorry, something went wrong. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    createSession();
  }, []);

  return (
    <div className="app">
      <aside className="sidebar">
        <h2>Lenny Assistant</h2>

        <button
          className="new-chat"
          onClick={createSession}
        >
          + New Chat
        </button>

        <div className="sidebar-info">
          Ask questions about product,
          growth, retention, PMF, and more.
        </div>
      </aside>

      <main className="chat-container">
        <header className="header">
          <h1>Lenny's Growth Assistant</h1>
          <p>
            Ask questions based on Lenny's Podcast transcripts.
          </p>
          {artifact && !showArtifact && (
  <button
    className="open-artifact"
    onClick={() => setShowArtifact(true)}
  >
    Open Artifact
  </button>
)}
        </header>

        <div className="messages">
          {messages.length === 0 && (
            <div className="welcome">
              <h2>What can I help you with?</h2>
              <p>
                Try asking:
              </p>

              <div className="suggestions">
                <button
                  onClick={() =>
                    setInput(
                      "How do I know if my product has product-market fit?"
                    )
                  }
                >
                  How do I know if I have PMF?
                </button>

                <button
                  onClick={() =>
                    setInput(
                      "How can I improve product retention?"
                    )
                  }
                >
                  How can I improve retention?
                </button>

                <button
                  onClick={() =>
                    setInput(
                      "What makes a great product manager?"
                    )
                  }
                >
                  What makes a great PM?
                </button>
              </div>
            </div>
          )}

          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.role}`}
            >
              <div className="message-label">
                {message.role === "user"
                  ? "You"
                  : "Lenny Assistant"}
              </div>

              <div className="message-content">
                {message.content}
              </div>

              {message.sources &&
                message.sources.length > 0 && (
                  <div className="sources">
                    <strong>Sources</strong>

                    {message.sources.map(
                      (source, sourceIndex) => (
                        <div
                          className="source"
                          key={sourceIndex}
                        >
                          <div>
                            <strong>
                              {source.guest}
                            </strong>{" "}
                            — {source.title}
                          </div>

                          {source.start_timestamp && (
                            <small>
                              {source.start_timestamp}
                            </small>
                          )}
                        </div>
                      )
                    )}
                  </div>
                )}
            </div>
          ))}

          {loading && (
            <div className="message assistant">
              <div className="message-label">
                Lenny Assistant
              </div>

              <div className="message-content">
                Thinking...
              </div>
            </div>
          )}
        </div>

        <div className="input-area">
          <textarea
            value={input}
            onChange={(e) =>
              setInput(e.target.value)
            }
            onKeyDown={(e) => {
              if (
                e.key === "Enter" &&
                !e.shiftKey
              ) {
                e.preventDefault();
                sendMessage();
              }
            }}
            placeholder="Ask Lenny something..."
            rows="2"
          />

          <button
            onClick={sendMessage}
            disabled={
              loading ||
              !input.trim() ||
              !sessionId
            }
          >
            Send
          </button>
        </div>
      </main>
      {artifact && showArtifact && (
  <aside className="artifact-panel">
    <div className="artifact-header">
      <h2>Artifact</h2>
      <button onClick={() => setShowArtifact(false)}>
        Close
      </button>
    </div>

    {artifact.type === "markdown" && (
      <pre className="markdown-artifact">
        {artifact.content}
      </pre>
    )}

    {artifact.type === "html" && (
      <iframe
        title="Generated artifact"
        srcDoc={artifact.content}
        sandbox=""
      />
    )}
  </aside>
)}
    </div>
  );
}

export default App;