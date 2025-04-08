import React from "react";

function Header() {
  return (
    <header className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-4 shadow-lg">
      <div className="max-w-6xl mx-auto px-4 flex justify-between items-center">
        <h1 className="text-2xl sm:text-3xl font-bold tracking-wide">
          Resume Optimizer 💼✨
        </h1>
        <div className="text-sm text-white/80 hidden sm:block">
          powered by <span className="font-semibold">FROST</span>
        </div>
      </div>
    </header>
  );
}

export default Header;
