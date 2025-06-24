import React, { useState } from "react";
import "../CSS/Settings.css"
import Profile from "../../assets/profile.png";
import imgs1 from "../../assets/s1.png";
import imgs2 from "../../assets/s2.png";
import imgs3 from "../../assets/s3.png";
import imgs4 from "../../assets/s4.png";
import imgs5 from "../../assets/s5.png";
import Ellipse from "../../assets/Ellipse.png";

export default function Settings() {
  // State for each toggle setting
  const [darkMode, setDarkMode] = useState(false);
  const [voiceInput, setVoiceInput] = useState(true);
  const [notifications, setNotifications] = useState(true);

  return (
    <div className="column_content_Settings">
      <div className="profile_container_Settings">
        <img
          src={Profile}
          className="profile_image_Settings"
        />
      </div>

      <div className="column_Settings">
        <span className="text_Settings">{"Settings"}</span>

        {/* Dark Mode Toggle */}
        <div className="view_Settings">
          <div className="row-view_Settings">
            <img
              src={imgs1}
              className="image_Settings"
            />
            <span className="input_Settings">Dark Mode</span>
            <div 
              className={darkMode ? "view3_Settings" : "view2_Settings"}
              onClick={() => setDarkMode(!darkMode)}
              style={{ cursor: 'pointer' }}
            >
              <img
                src={Ellipse}
                className="image2_Settings"
              />
            </div>
          </div>
        </div>

        {/* Voice Input Toggle */}
        <div className="view_Settings">
          <div className="row-view2_Settings">
            <img
              src={imgs2}
              className="image3_Settings"
            />
            <span className="input_Settings">Voice Input</span>
            <div 
              className={voiceInput ? "view3_Settings" : "view2_Settings"}
              onClick={() => setVoiceInput(!voiceInput)}
              style={{ cursor: 'pointer' }}
            >
              <img
                src={Ellipse}
                className="image2_Settings"
              />
            </div>
          </div>
        </div>

        {/* Notifications Toggle */}
        <div className="view4_Settings">
          <div className="row-view3_Settings">
            <img
              src={imgs3}
              className="image4_Settings"
            />
            <span className="input2_Settings">Notifications</span>
            <div 
              className={notifications ? "view5_Settings" : "view2_Settings"}
              onClick={() => setNotifications(!notifications)}
              style={{ cursor: 'pointer' }}
            >
              <img
                src={Ellipse}
                className="image2_Settings"
              />
            </div>
          </div>
        </div>

        {/* Language Setting (non-interactive) */}
        <div className="view6_Settings">
          <div className="row-view4_Settings">
            <img
              src={imgs4}
              className="image_Settings"
            />
            <span className="text2_Settings">Language</span>
            <span className="text3_Settings">English</span>
          </div>
        </div>

        {/* Reset Settings Button */}
        <button 
          className="button_Reset_Settings"
          onClick={() => {
            setDarkMode(false);
            setVoiceInput(false);
            setNotifications(false);
            alert("Settings have been reset!");
          }}
        >
          <div className="row-view_Reset_Settings">
            <img
              src={imgs5}
              className="image_Reset_Settings"
            />
            <div className="box_Reset_Settings"></div>
            <span className="text_Reset_Settings">
              {"Reset Settings"}
            </span>
          </div>
        </button>
      </div>
    </div>
  )
}