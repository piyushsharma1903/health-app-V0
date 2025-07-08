// src/App.js
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import UploadForm from "./pages/UploadForm";
import Reports from "./pages/Reports";
import Dashboard from "./pages/Dashboard";
import Tracker from "./pages/Tracker";

function App() {
  return (
    <Router>
      <Navbar /> {/* 🧠 Navbar shown on all pages */}
      <Routes>
        <Route path="/" element={<UploadForm />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/tracker" element={<Tracker />} />
      </Routes>
    </Router>
  );
}

export default App;
