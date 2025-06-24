import React from "react";
import { Link, useLocation } from "react-router-dom";
import "../CSS/sidebar1.css";
import Switch from "../../assets/switch.png";
import Home from "../../assets/home.png";
import About from "../../assets/about.png";
import Help from "../../assets/help.png";
import Settings from "../../assets/settings.png";
import Logout from "../../assets/logout.png";

export default function Sidebar1() {
    const location = useLocation();
    
    return (
        <div className="column_Sidebar1">
            {/* Toggle to sidebar2 view */}
            <Link to={location.pathname === '/' ? '/compact' : `/compact${location.pathname}`}>
                <div className="view_Sidebar1">
                    <img
                        src={Switch}
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
                    src={Home}
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
                    src={About}
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
                    src={Help}
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
                    src={Settings}
                    className="image4_Sidebar1"
                    alt="Settings"
                />
                <span className="text_Sidebar1">Settings</span>
            </Link>

            <div className="row-view4_Sidebar1" onClick={() => {/* Add logout logic here */}}>
                <img
                    src={Logout}
                    className="image4_Sidebar1"
                    alt="Logout"
                />
                <span className="text_Sidebar1">Logout</span>
            </div>
        </div>
    );
}