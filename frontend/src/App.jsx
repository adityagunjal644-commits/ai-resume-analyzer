import { useState } from "react";
import "./App.css";

const RING_LENGTH = 339.29; // circumference of the score ring (r = 54)
const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function getVerdict(score) {
  if (score >= 80) return { label: "Strong match", color: "#0f766e" };
  if (score >= 50) return { label: "Decent match", color: "#a16207" };
  return { label: "Low match", color: "#b4432e" };
}

// Turns the AI's plain text into sections: [{ title, items }]
function parseFeedback(text) {
  const headings = ["Summary", "Resume Improvements", "Next Steps"];
  const sections = [];
  let current = null;

  for (const raw of text.split("\n")) {
    const line = raw.trim();
    if (!line) continue;

    const cleaned = line.replace(/[:*#]/g, "").trim();
    if (headings.includes(cleaned)) {
      current = { title: cleaned, items: [] };
      sections.push(current);
    } else if (current) {
      current.items.push(line.replace(/^[-*•]\s*/, ""));
    }
  }
  return sections;
}

function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [isOver, setIsOver] = useState(false);

  function pickFile(selected) {
    if (!selected.name.toLowerCase().endsWith(".pdf")) {
      setError("That file is not a PDF. Upload your resume as a PDF.");
      return;
    }
    setError("");
    setFile(selected);
  }

  function handleDrop(e) {
    e.preventDefault();
    setIsOver(false);
    const dropped = e.dataTransfer.files[0];
    if (dropped) pickFile(dropped);
  }

  async function handleAnalyze() {
    if (!file || !jobDescription.trim()) {
      setError("Add a PDF resume and a job description to continue.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_description", jobDescription);

    try {
      const res = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "The analysis failed. Try again.");
      }

      setResult(await res.json());
    } catch (err) {
      setError(
        err.message === "Failed to fetch"
          ? "Cannot reach the server. Check that the backend is running."
          : err.message
      );
    } finally {
      setLoading(false);
    }
  }

  const aiSections = result?.ai_feedback ? parseFeedback(result.ai_feedback) : [];
  const verdict = result ? getVerdict(result.score) : null;
  const totalSkills = result ? result.job_skills.length : 0;

  return (
    <div className="app">
      <header className="topbar">
        <div className="topbar-inner">
          <span className="brand">
            <svg
              width="22"
              height="22"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.8"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <path d="M6 3h8l5 5v13H6z" />
              <path d="M14 3v5h5" />
              <path d="M9.5 13h6M9.5 17h6" />
            </svg>
            AI Resume Analyzer
          </span>
        </div>
      </header>

      <main className="layout">
        <section className="panel input-panel">
          <h1>See how your resume fits the job</h1>
          <p className="lede">
            Upload your resume and paste a job description. You get a match
            score, the skills you are missing, and a written review.
          </p>

          <div className="field">
            <span className="field-label" id="resume-label">
              Resume (PDF)
            </span>
            <label
              className={`dropzone${isOver ? " is-over" : ""}`}
              onDragOver={(e) => {
                e.preventDefault();
                setIsOver(true);
              }}
              onDragLeave={() => setIsOver(false)}
              onDrop={handleDrop}
            >
              <input
                type="file"
                accept=".pdf,application/pdf"
                aria-labelledby="resume-label"
                onChange={(e) => e.target.files[0] && pickFile(e.target.files[0])}
              />
              <span className="dropzone-icon">
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  aria-hidden="true"
                >
                  <path d="M12 16V5M7.5 9.5 12 5l4.5 4.5M5 19h14" />
                </svg>
              </span>
              <span className="dropzone-text">
                <strong>{file ? file.name : "Choose a PDF or drop it here"}</strong>
                <span>{file ? "Select to replace" : "Text-based PDFs work best"}</span>
              </span>
            </label>
          </div>

          <div className="field">
            <label className="field-label" htmlFor="jd">
              Job description
            </label>
            <textarea
              id="jd"
              className="textarea"
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the full job posting, including the requirements."
            />
          </div>

          <button className="btn-primary" onClick={handleAnalyze} disabled={loading}>
            {loading && <span className="spinner" aria-hidden="true" />}
            {loading ? "Analyzing…" : "Analyze resume"}
          </button>

          {error && (
            <p className="error" role="alert">
              {error}
            </p>
          )}
        </section>

        <section className="results" aria-live="polite">
          {loading && (
            <div className="panel state">
              <span className="spinner spinner-dark" aria-hidden="true" />
              <h2>Analyzing your resume</h2>
              <p>
                Reading your resume and comparing it with the job. The written
                review can take up to 30 seconds.
              </p>
            </div>
          )}

          {!loading && !result && (
            <div className="panel state">
              <h2>Your results appear here</h2>
              <p>
                Add a resume and a job description, then select Analyze resume.
                You will get:
              </p>
              <ul className="list">
                <li>A match score out of 100</li>
                <li>The skills you have and the ones you are missing</li>
                <li>A written review with next steps</li>
              </ul>
            </div>
          )}

          {!loading && result && (
            <article className="panel results-panel">
              <div className="block">
                <div className="score-row" style={{ "--ring-color": verdict.color }}>
                  <div className="ring">
                    <svg viewBox="0 0 128 128" aria-hidden="true">
                      <circle className="ring-track" cx="64" cy="64" r="54" />
                      <circle
                        className="ring-fill"
                        cx="64"
                        cy="64"
                        r="54"
                        style={{ "--target": RING_LENGTH * (1 - result.score / 100) }}
                      />
                    </svg>
                    <div className="ring-value">
                      <span className="ring-number">
                        {result.score}
                        <small>%</small>
                      </span>
                    </div>
                  </div>
                  <div className="score-copy">
                    <h2>{verdict.label}</h2>
                    <p>
                      {totalSkills > 0
                        ? `${result.matched_skills.length} of ${totalSkills} skills the job asks for appear in your resume.`
                        : "No known skills were found in this job description. Paste the full posting and try again."}
                    </p>
                  </div>
                </div>
              </div>

              <div className="block">
                <div className="skills-grid">
                  <div>
                    <h3>Matched skills</h3>
                    {result.matched_skills.length === 0 ? (
                      <p className="empty-note">No matching skills found.</p>
                    ) : (
                      <div className="chips">
                        {result.matched_skills.map((s) => (
                          <span key={s} className="chip chip-match">
                            {s}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                  <div>
                    <h3>Missing skills</h3>
                    {result.missing_skills.length === 0 ? (
                      <p className="empty-note">Nothing missing. Great match.</p>
                    ) : (
                      <div className="chips">
                        {result.missing_skills.map((s) => (
                          <span key={s} className="chip chip-missing">
                            {s}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </div>

              <div className="block">
                <div className="two-col">
                  <div>
                    <h3>What is working</h3>
                    <ul className="list">
                      {result.strengths.length === 0 && (
                        <li>No strengths detected yet. Add the required skills.</li>
                      )}
                      {result.strengths.map((s, i) => (
                        <li key={i}>{s}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h3>How to improve</h3>
                    <ul className="list list-improve">
                      {result.suggestions.map((s, i) => (
                        <li key={i}>{s}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>

              <div className="block ai-block">
                <h3>AI review</h3>
                {aiSections.length > 0 ? (
                  <>
                    {aiSections.map((section) => (
                      <div className="ai-section" key={section.title}>
                        <h4>{section.title}</h4>
                        <ul className="list">
                          {section.items.map((item, i) => (
                            <li key={i}>{item}</li>
                          ))}
                        </ul>
                      </div>
                    ))}
                    <p className="ai-note">
                      AI feedback can miss context. Check it against your own
                      experience before you change your resume.
                    </p>
                  </>
                ) : (
                  <p className="empty-note">
                    The AI review is unavailable right now. Your score and skill
                    results above are still valid. Try again in a minute.
                  </p>
                )}
              </div>
            </article>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;