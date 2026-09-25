import { useState } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState(
    "Machine 7 keeps stopping. Why?"
  );
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function askForgeBridge() {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ question })
      });

      if (!response.ok) {
        throw new Error("Backend request failed");
      }

      const data = await response.json();
      setResult(data);
    } catch {
      setError(
        "Could not connect to the backend. Confirm that Uvicorn is running on port 8000."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app">
      <header>
        <p className="label">FORGEBRIDGE AI</p>
        <h1>Legacy Automotive Intelligence</h1>
        <p>
          Understand, troubleshoot, secure, and modernize fictional legacy
          factory software.
        </p>
      </header>

      <div className="warning">
        Fictional demonstration data — not real factory evidence.
      </div>

      <section className="card">
        <h2>Ask ForgeBridge</h2>

        <textarea
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          rows="4"
        />

        <button onClick={askForgeBridge} disabled={loading}>
          {loading ? "Analyzing..." : "Analyze"}
        </button>

        {error && <p className="error">{error}</p>}
      </section>

      {result && (
        <section className="card">
          <h2>Answer</h2>
          <p>{result.answer}</p>

          <h2>Agent findings</h2>

          {result.agents.map((agent, index) => (
            <article className="finding" key={`${agent.agent}-${index}`}>
              <h3>{agent.agent}</h3>

              {agent.language && (
                <p>
                  <strong>Language:</strong> {agent.language}
                </p>
              )}

              <p>{agent.finding}</p>

              <p>
                <strong>Status:</strong> {agent.status}
              </p>

              <h4>Sources</h4>
              <ul>
                {agent.sources.map((source) => (
                  <li key={source}>{source}</li>
                ))}
              </ul>
            </article>
          ))}
        </section>
      )}

      <section className="card">
        <h2>Project modules</h2>

        <div className="modules">
          <span>Legacy Analysis</span>
          <span>History</span>
          <span>Architecture</span>
          <span>Security</span>
          <span>Migration</span>
        </div>
      </section>
    </main>
  );
}

export default App;