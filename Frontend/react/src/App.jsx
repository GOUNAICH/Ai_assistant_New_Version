import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Sidebar from "./components/JSX/Sidebar";
import MainContent from "./components/JSX/MainContent";
import About from "./components/JSX/About";
import Help from "./components/JSX/Help";
import Settings from "./components/JSX/Settings";

export default function App() {
  return (
    <Router>
      <div className="app-container">
        <Sidebar />
        <Routes>
          <Route path="/" element={<MainContent />} />
          <Route path="/about" element={<About />} />
          <Route path="/help" element={<Help />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </div>
    </Router>
  );
}
