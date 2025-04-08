import React, { useState } from "react";
import axios from "axios";

function JDInput() {
  const [jobDescription, setJobDescription] = useState("");
  const [resumeText, setResumeText] = useState(""); // TEMP: manually paste
  const [scoreResult, setScoreResult] = useState(null);

  const handleScore = async () => {
    if (!resumeText || !jobDescription) {
      alert("Please paste both resume and JD.");
      return;
    }
  
    try {
      // Step 1: Store the JD in backend
      const jdForm = new FormData();
      jdForm.append("user_id", "sakthisharanm@gmail.com");
      jdForm.append("jd_text", jobDescription);
  
      await axios.post("http://localhost:8000/upload-job-description", jdForm);
  
      // Step 2: Send resume for scoring
      const scoreForm = new FormData();
      scoreForm.append("user_id", "sakthisharanm@gmail.com");
      scoreForm.append("resume_text", resumeText);
  
      const response = await axios.post("http://localhost:8000/score-resume", scoreForm);
  
      setScoreResult(response.data);
    } catch (err) {
      console.error("Scoring failed:", err);
      alert("Failed to score resume.");
    }
  };
  
  return (
    <div className="bg-white p-6 mt-6 rounded-xl shadow-md">
      <h2 className="text-xl font-bold mb-2 text-gray-800">📄 Paste Job Description</h2>
      <textarea
        rows={5}
        className="w-full border rounded p-2 mb-4"
        placeholder="Paste job description here..."
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
      />

      <textarea
        rows={4}
        className="w-full border rounded p-2 mb-4"
        placeholder="Paste resume text here (for now)"
        value={resumeText}
        onChange={(e) => setResumeText(e.target.value)}
      />

      <button
        className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
        onClick={handleScore}
      >
        🎯 Score Resume
      </button>

      {scoreResult && (
        <div className="mt-6 bg-gray-50 p-4 rounded">
          <p className="font-semibold text-lg text-gray-700">
            🧠 Score: {scoreResult.score} / 100
          </p>
          <p className="text-green-700 mt-2">
            ✅ Matched: {scoreResult.matched_keywords.join(", ")}
          </p>
          <p className="text-red-600 mt-1">
            ❌ Missing: {scoreResult.missing_keywords.join(", ")}
          </p>
        </div>
      )}
    </div>
  );
}

export default JDInput;
