// src/components/Navbar.js
import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav style={{ padding: "1rem", borderBottom: "1px solid #ddd" }}>
      <Link to="/" style={{ marginRight: "1rem" }}>Upload</Link>
      <Link to="/reports" style={{ marginRight: "1rem" }}>Reports</Link>
      <Link to="/dashboard" style={{ marginRight: "1rem" }}>Dashboard</Link>
      <Link to="/tracker">Tracker</Link>
    </nav>
  );
};

export default Navbar;
