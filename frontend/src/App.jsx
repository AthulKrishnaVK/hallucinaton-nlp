import { useState } from "react";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
const analyzeText = async () => {
  if (!text.trim()) {
    setError("Please enter some text to analyze.");
    return;
  }

  setLoading(true);
  setError("");
  setResult(null);

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/api/analyze",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: text,
        }),
      }
    );

    // Get response body even when status is an error
    const responseText = await response.text();

    console.log("Backend status:", response.status);
    console.log("Backend response:", responseText);

    if (!response.ok) {
      throw new Error(
        `Backend returned ${response.status}: ${responseText}`
      );
    }

    const data = JSON.parse(responseText);

    setResult(data);

  } catch (err) {
    console.error("Analysis error:", err);

    setError(
      err.message ||
      "Unable to connect to the backend."
    );

  } finally {
    setLoading(false);
  }
};

  const getStatusClass = (status) => {
    if (status === "supported") {
      return "supported";
    }

    if (status === "hallucinated") {
      return "hallucinated";
    }

    return "unverified";
  };

  return (
    <div className="app">

      {/* Header */}

      <header className="header">
        <div>
          <h1>Hallucination Detector</h1>

          <p>
            Detect unsupported and contradictory claims
            in LLM-generated text.
          </p>
        </div>
      </header>


      {/* Main */}

      <main className="container">

        {/* Input Section */}

        <section className="card">

          <h2>Analyze Text</h2>

          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste an LLM-generated response here..."
          />

          <button
            onClick={analyzeText}
            disabled={loading}
          >
            {loading
              ? "Analyzing..."
              : "Analyze Text"}
          </button>

          {error && (
            <div className="error">
              {error}
            </div>
          )}

        </section>


        {/* Results */}

        {result && (
          <section className="results">

            {/* Overall Score */}

            <div className="score-card">

              <div>
                <h2>Overall Result</h2>

                <p>
                  {result.overall.total_claims} claims
                  analyzed
                </p>
              </div>

              <div className="score">

                <span>
                  {result.overall.hallucination_percentage}%
                </span>

                <small>
                  Hallucination
                </small>

              </div>

            </div>


            {/* Claim Results */}

            <div className="card">

              <h2>Claim Analysis</h2>

              {result.claims.length === 0 ? (
                <p>
                  No factual claims were detected.
                </p>
              ) : (
                <div className="claims">

                  {result.claims.map((claim) => (

                    <div
                      className="claim"
                      key={claim.id}
                    >

                      <div className="claim-header">

                        <span className="claim-number">
                          Claim {claim.id}
                        </span>

                        <span
                          className={`status ${getStatusClass(
                            claim.verification.status
                          )}`}
                        >
                          {claim.verification.status}
                        </span>

                      </div>


                      <p className="claim-text">
                        {claim.claim}
                      </p>


                      <div className="confidence">

                        <strong>
                          Confidence:
                        </strong>{" "}

                        {(
                          claim.verification.confidence *
                          100
                        ).toFixed(2)}
                        %

                      </div>


                      {/* Evidence */}

                      <div className="evidence">

                        <h3>
                          Evidence
                        </h3>

                        {claim.evidence.length === 0 ? (

                          <p>
                            No evidence found.
                          </p>

                        ) : (

                          claim.evidence.map(
                            (item, index) => (

                              <div
                                className="evidence-item"
                                key={index}
                              >

                                <p>
                                  {item.text}
                                </p>

                                <div className="evidence-meta">

                                  <span>
                                    Source:{" "}
                                    {item.source ||
                                      "Unknown"}
                                  </span>

                                  {item.similarity !==
                                    null &&
                                    item.similarity !==
                                      undefined && (
                                      <span>
                                        Similarity:{" "}
                                        {(
                                          item.similarity *
                                          100
                                        ).toFixed(1)}
                                        %
                                      </span>
                                    )}

                                  {item.url && (
                                    <a
                                      href={item.url}
                                      target="_blank"
                                      rel="noreferrer"
                                    >
                                      View source
                                    </a>
                                  )}

                                </div>

                              </div>

                            )
                          )

                        )}

                      </div>

                    </div>

                  ))}

                </div>
              )}

            </div>

          </section>
        )}

      </main>

    </div>
  );
}

export default App;