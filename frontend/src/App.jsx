import { useState } from "react";
import "./App.css";

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

  async function handleAnalyze() {
    if (!file || !jobDescription.trim()) {
      setError("Please upload a PDF resume and paste a job description.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_description", jobDescription);

    try {
      const res = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Something went wrong");
      }

      setResult(await res.json());
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  const aiSections = result?.ai_feedback ? parseFeedback(result.ai_feedback) : [];

  return (
    <div className="container">
      <h1>AI Resume Analyzer</h1>

      <div className="card">
        <h3>1. Upload your resume (PDF)</h3>
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />
      </div>

      <div className="card">
        <h3>2. Paste the job description</h3>
        <textarea
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          placeholder="Paste the job description here..."
        />
      </div>

      <button onClick={handleAnalyze} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze"}
      </button>
      {loading && (
        <p className="muted">The AI review can take up to 30 seconds.</p>
      )}

      {error && <p className="error">{error}</p>}

      {result && (
        <>
          <div className="card" style={{ marginTop: 20 }}>
            <h3>ATS Match Score</h3>
            <div className="score">{result.score}%</div>

            <h3>Matched Skills</h3>
            {result.matched_skills.length === 0 && <p>None found</p>}
            {result.matched_skills.map((s) => (
              <span key={s} className="tag match">{s}</span>
            ))}

            <h3>Missing Skills</h3>
            {result.missing_skills.length === 0 && <p>None. Great match!</p>}
            {result.missing_skills.map((s) => (
              <span key={s} className="tag missing">{s}</span>
            ))}

            <h3>Strengths</h3>
            <ul>
              {result.strengths.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ul>

            <h3>How to Improve</h3>
            <ul>
              {result.suggestions.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
          </div>

          <div className="card ai-card">
            <h3>AI Review</h3>
            {aiSections.length > 0 ? (
              aiSections.map((section) => (
                <div key={section.title}>
                  <h4>{section.title}</h4>
                  <ul>
                    {section.items.map((item, i) => (
                      <li key={i}>{item}</li>
                    ))}
                  </ul>
                </div>
              ))
            ) : (
              <p className="muted">
                AI review is unavailable right now. The results above are still
                valid. Try again in a minute.
              </p>
            )}
          </div>
        </>
      )}
    </div>
  );
}

export default App;