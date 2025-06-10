import React from "react";
import { Link, useLocation } from "react-router-dom";
import "../CSS/sidebar2.css";

export default function Sidebar2() {
    const location = useLocation();
    
    return (
        <div className="column_Sidebar2">
            {/* Toggle back to sidebar1 view */}
            <Link to={location.pathname === '/compact' ? '/' : location.pathname.replace('/compact', '')}>
                <img
                    src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/803gsj8h_expires_30_days.png"
                    className="image_Sidebar2"
                    alt="Switch to expanded view"
                />
            </Link>

            <Link 
                to="/compact"
                className={location.pathname === '/compact' ? 'active' : ''}
            >
                <img
                    src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/qabgol9l_expires_30_days.png"
                    className="image2_Sidebar2"
                    alt="Home"
                />
            </Link>

            <Link 
                to="/compact/about"
                className={location.pathname === '/compact/about' ? 'active' : ''}
            >
                <img
                    src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/gp6rafj3_expires_30_days.png"
                    className="image3_Sidebar2"
                    alt="About"
                />
            </Link>

            <Link 
                to="/compact/help"
                className={location.pathname === '/compact/help' ? 'active' : ''}
            >
                <img
                    src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/26ngz7mg_expires_30_days.png"
                    className="image4_Sidebar2"
                    alt="Help"
                />
            </Link>

            <Link 
                to="/compact/settings"
                className={location.pathname === '/compact/settings' ? 'active' : ''}
            >
                <img
                    src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/j9pywe9q_expires_30_days.png"
                    className="image5_Sidebar2"
                    alt="Settings"
                />
            </Link>

            <div onClick={() => {/* Add logout logic here */}}>
                <img
                    src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/djpqphve_expires_30_days.png"
                    className="image6_Sidebar2"
                    alt="Logout"
                />
            </div>
        </div>
    );
}