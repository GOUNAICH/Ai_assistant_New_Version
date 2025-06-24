import React from "react";
import { Link, useLocation } from "react-router-dom";
import "../CSS/sidebar2.css";
import Switch from "../../assets/switch.png";
import Home from "../../assets/home.png";
import About from "../../assets/about.png";
import Help from "../../assets/help.png";
import Settings from "../../assets/settings.png";
import Logout from "../../assets/logout.png";

export default function Sidebar2() {
    const location = useLocation();

    return (
        <div className="column_Sidebar2">
            {/* Toggle back to sidebar1 view */}
            <Link to={location.pathname === '/compact' ? '/' : location.pathname.replace('/compact', '')}>
                <img
                    src={Switch}
                    className="image_Sidebar2"
                    alt="Switch to expanded view"
                />
            </Link>

            <Link
                to="/compact"
                className={location.pathname === '/compact' ? 'active' : ''}
            >
                <img
                    src={Home}
                    className="image2_Sidebar2"
                    alt="Home"
                />
            </Link>

            <Link
                to="/compact/about"
                className={location.pathname === '/compact/about' ? 'active' : ''}
            >
                <img
                    src={About}
                    className="image3_Sidebar2"
                    alt="About"
                />
            </Link>

            <Link
                to="/compact/help"
                className={location.pathname === '/compact/help' ? 'active' : ''}
            >
                <img
                    src={Help}
                    className="image4_Sidebar2"
                    alt="Help"
                />
            </Link>

            <Link
                to="/compact/settings"
                className={location.pathname === '/compact/settings' ? 'active' : ''}
            >
                <img
                    src={Settings}
                    className="image5_Sidebar2"
                    alt="Settings"
                />
            </Link>

            <div onClick={() => {/* Add logout logic here */ }}>
                <img
                    src={Logout}
                    className="image6_Sidebar2"
                    alt="Logout"
                />
            </div>
        </div>
    );
}