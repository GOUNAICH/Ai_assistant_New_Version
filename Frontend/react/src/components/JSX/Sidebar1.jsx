import React from "react";
import { Link, useLocation } from "react-router-dom";
import "../CSS/sidebar1.css";

export default function Sidebar1() {
    const location = useLocation();
    
    return (
        <div className="column_Sidebar1">
            {/* Toggle to sidebar2 view */}
            <Link to={location.pathname === '/' ? '/compact' : `/compact${location.pathname}`}>
                <div className="view_Sidebar1">
                    <img
                        src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/kjsbh6ag_expires_30_days.png"
                        className="image_Sidebar1"
                        alt="Switch to compact view"
                    />
                </div>
            </Link>

            <Link 
                to="/" 
                className={`row-view_Sidebar1 ${location.pathname === '/' ? 'active' : ''}`}
            >
                <img
                    src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/i1mbnej5_expires_30_days.png"
                    className="image2_Sidebar1"
                    alt="Home"
                />
                <span className="text_Sidebar1">Home</span>
            </Link>

            <Link 
                to="/about" 
                className={`row-view2_Sidebar1 ${location.pathname === '/about' ? 'active' : ''}`}
            >
                <img
                    src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/n04crih1_expires_30_days.png"
                    className="image3_Sidebar1"
                    alt="About"
                />
                <span className="text2_Sidebar1">About</span>
            </Link>

            <Link 
                to="/help" 
                className={`row-view_Sidebar1 ${location.pathname === '/help' ? 'active' : ''}`}
            >
                <img
                    src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/kdfjitjs_expires_30_days.png"
                    className="image4_Sidebar1"
                    alt="Help"
                />
                <span className="text3_Sidebar1">Help</span>
            </Link>

            <Link 
                to="/settings" 
                className={`row-view3_Sidebar1 ${location.pathname === '/settings' ? 'active' : ''}`}
            >
                <img
                    src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/e81dco88_expires_30_days.png"
                    className="image4_Sidebar1"
                    alt="Settings"
                />
                <span className="text_Sidebar1">Settings</span>
            </Link>

            <div className="row-view4_Sidebar1" onClick={() => {/* Add logout logic here */}}>
                <img
                    src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/3d7314jf_expires_30_days.png"
                    className="image4_Sidebar1"
                    alt="Logout"
                />
                <span className="text_Sidebar1">Logout</span>
            </div>
        </div>
    );
}