import React from "react";
import { Link } from "react-router-dom";
import "../CSS/sidebar.css";

export default function Sidebar() {
  return (
    <div className="column">
      <Link to="/" className="row-view2">
        <img
          src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/24njmecx_expires_30_days.png"
          className="image"
        />
        <span className="text">Home</span>
      </Link>
      <Link to="/about" className="row-view3">
        <img
          src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/nio4ejqu_expires_30_days.png"
          className="image"
        />
        <span className="text">About</span>
      </Link>
      <Link to="/help" className="row-view4">
        <img
          src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/442pfej1_expires_30_days.png"
          className="image"
        />
        <span className="text">Help</span>
      </Link>
      <Link to="/settings" className="row-view5">
        <img
          src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/00gisola_expires_30_days.png"
          className="image"
        />
        <span className="text">Settings</span>
      </Link>
    </div>
  );
}
