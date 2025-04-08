import React, { useState } from "react";
import ResumeUpload from "./components/ResumeUpload";
import JDInput from "./components/JDInput";

function App() {
  const [resumeText, setResumeText] = useState(""); // shared resume text

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold">Resume Optimizer 💼</h1>
      <p className="text-gray-600 mb-6">powered by FROST</p>

      {/* send setResumeText into ResumeUpload */}
      <ResumeUpload setResumeText={setResumeText} />

      {/* send resumeText into JDInput */}
      <JDInput resumeText={resumeText} />
    </div>
  );
}

export default App;
