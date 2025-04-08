import React from "react";
import { CircularProgressbar, buildStyles } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";

function ScoreVisualizer({ score }) {
  // Determine color based on score
  let color = "#22c55e"; // green
  if (score < 50) color = "#ef4444"; // red
  else if (score < 80) color = "#facc15"; // yellow

  return (
    <div className="w-40 mx-auto my-6">
      <CircularProgressbar
        value={score}
        text={`${score}%`}
        styles={buildStyles({
          textColor: "#1f2937", // text-gray-800
          pathColor: color,
          trailColor: "#e5e7eb", // gray-200
          textSize: "16px"
        })}
      />
      <p className="text-center mt-2 font-semibold text-gray-700">
        ATS Score
      </p>
    </div>
  );
}

export default ScoreVisualizer;
