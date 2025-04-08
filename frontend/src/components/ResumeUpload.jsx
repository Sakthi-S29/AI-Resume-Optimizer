import React, { useState } from "react";
import axios from "axios";

function ResumeUpload() {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setUploadStatus("");
  };

  const handleUpload = async () => {
    if (!file) {
      setUploadStatus("Please select a resume to upload.");
      return;
    }

    const formData = new FormData();
    formData.append("resume", file);

    try {
      const response = await axios.post("http://localhost:8000/upload-resume", formData);
      setUploadStatus("✅ Resume uploaded successfully");
      console.log(response.data);
    } catch (error) {
      console.error("Upload failed:", error);
      setUploadStatus("❌ Upload failed. Try again.");
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-md mt-8">
      <h2 className="text-lg font-semibold text-gray-800 mb-4">Upload Your Resume</h2>
      
      <div className="flex flex-col sm:flex-row items-center gap-4">
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          className="border p-2 rounded w-full sm:w-auto"
        />
        <button
          onClick={handleUpload}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Upload Resume
        </button>
      </div>

      {uploadStatus && (
        <p className="mt-4 text-sm text-gray-700">{uploadStatus}</p>
      )}
    </div>
  );
}

export default ResumeUpload;
