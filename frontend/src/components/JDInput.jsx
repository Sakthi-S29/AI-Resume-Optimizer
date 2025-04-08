import React, { useState } from "react";
import axios from "axios";
import ScoreVisualizer from "./ScoreVisualizer";

function JDInput({ resumeText }) {
  const [jobDescription, setJobDescription] = useState("");
  const [scoreResult, setScoreResult] = useState(null);

  const handleScore = async () => {
    if (!jobDescription) {
      alert("Please paste JD.");
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

      <button
        className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
        onClick={handleScore}
      >
        🎯 Score Resume
      </button>

      {scoreResult && (
  <div className="mt-6 bg-gray-50 p-4 rounded">
    <ScoreVisualizer score={scoreResult.score} />

    <p className="text-green-700 mt-2">
      ✅ Matched: {scoreResult.matched_keywords.join(", ")}
    </p>
    <p className="text-red-600 mt-1">
      ❌ Missing: {scoreResult.missing_keywords.join(", ")}
    </p>
    {scoreResult.suggestions && (
  <div className="mt-4">
    <h3 className="font-bold text-gray-800 mb-2">💡 Suggestions:</h3>
    <ul className="list-disc list-inside space-y-1 text-gray-700">
      {Object.entries(scoreResult.suggestions).map(([keyword, tip]) => (
        <li key={keyword}>
          <span className="font-semibold">{keyword}:</span> {tip}
        </li>
      ))}
    </ul>
  </div>
)}
  </div>
)}

    </div>
  );
}

export default JDInput;
