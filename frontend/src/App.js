import React from "react";
import Header from "./components/Header";
import ResumeUpload from "./components/ResumeUpload";
import JDInput from "./components/JDInput";

function App() {
  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold">Resume Optimizer 💼✨</h1>
      <p className="text-gray-600 mt-2">powered by FROST</p>
      <p className="mb-6">Let’s optimize your resume 🚀</p>

      <ResumeUpload />
      <JDInput />
    </div>
  );
}

export default App;
