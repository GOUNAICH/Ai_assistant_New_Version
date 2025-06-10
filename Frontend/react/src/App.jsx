import React from "react";
import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";
import MainContent from "./components/JSX/MainContent";
import About from "./components/JSX/About";
import Help from "./components/JSX/Help";
import Settings from "./components/JSX/Settings";
import Sidebar1 from "./components/JSX/Sidebar1";
import Sidebar2 from "./components/JSX/Sidebar2";

function Layout() {
  const location = useLocation();
  
  // Check if we're in compact/sidebar2 mode
  // This will be true for any route that starts with "/compact"
  const showSidebar2 = location.pathname.startsWith("/compact");

  return (
    <div className="app-container">
      {showSidebar2 ? <Sidebar2 /> : <Sidebar1 />}
      <Routes>
        {/* Regular routes with Sidebar1 */}
        <Route path="/" element={<MainContent />} />
        <Route path="/about" element={<About />} />
        <Route path="/help" element={<Help />} />
        <Route path="/settings" element={<Settings />} />
        
        {/* Compact routes with Sidebar2 */}
        <Route path="/compact" element={<MainContent />} />
        <Route path="/compact/about" element={<About />} />
        <Route path="/compact/help" element={<Help />} />
        <Route path="/compact/settings" element={<Settings />} />
      </Routes>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <Layout />
    </Router>
  );
}