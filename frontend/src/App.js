import React from "react";
import Header from "./components/Header";
import ResumeUpload from "./components/ResumeUpload";

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="max-w-4xl mx-auto p-6">
  <div className="text-xl font-semibold text-gray-700 mt-4">
    Let’s optimize your resume 🚀
  </div>
  <ResumeUpload />
</main>
    </div>
  );
}

export default App;
