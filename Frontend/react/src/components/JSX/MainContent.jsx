import React, { useEffect, useState } from "react";
import group7Img from "../../assets/Group 6.png";
import "../CSS/maincontent.css";

export default function MainContent() {
  const [input1, onChangeInput1] = useState("");
  const [response, setResponse] = useState("Hello, How can I assist you today?");
  const [isListening, setIsListening] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);
  const [lastUserMessage, setLastUserMessage] = useState("");

  useEffect(() => {
    if (window.electron) {
      if (!isInitialized) {
        window.electron.sendMessage("electron-ready");
        setIsInitialized(true);
      }

      const handlePythonResponse = (data) => {
        console.log("Received from Python:", data);

        if (data.includes("Listening...")) {
          setIsListening(true);
          setResponse("Listening...");
        } else if (data && data.trim()) {
          setIsListening(false);
          setResponse(data.trim());
        }
      };

      const handleUserMessage = (message) => {
        setLastUserMessage(`User: ${message}`);
      };

      window.electron.onMessage("python-response", handlePythonResponse);
      window.electron.onMessage("user-message", handleUserMessage);

      // NO cleanup here because removeMessageListener is NOT available in your preload.js
    }
  }, [isInitialized]);

  return (
    <div className="column_content">
      <div className="profile_container">
        <img
          src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/tlstigkr_expires_30_days.png"
          className="profile_image"
          alt="Profile"
        />
      </div>

      <div className="centered_text_container">
        <span
          className="text_content"
          style={{
            whiteSpace: "pre-line",
            color: response === "Listening..." ? "#736AF4" : undefined,
          }}
        >
          {lastUserMessage ? `${lastUserMessage}\n` : ""}
          {response}
        </span>
      </div>

      <div className="column2_content">
        <img src={group7Img} alt="Group 7" />
      </div>

      <div className="view_content">
        <div className="row-view2_content">
          <input
            placeholder="Ask me anything . . ."
            value={input1}
            onChange={(e) => onChangeInput1(e.target.value)}
            className="input_content"
          />
          <img
            src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/jf2awte7_expires_30_days.png"
            className="image3_content"
            alt="Icon 1"
          />
          <img
            src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/qorxs7lm_expires_30_days.png"
            className="image4_content"
            alt="Icon 2"
          />
        </div>
      </div>

      <div className="row-view3_content">
        <button className="column3_content">
          <img
            src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/3ppmif4e_expires_30_days.png"
            className="image5_content"
            alt="Weather"
          />
          <span className="text3_content">Weather</span>
        </button>
        <button className="button-column_content" onClick={() => alert("Pressed!")}>
          <img
            src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/vck604ua_expires_30_days.png"
            className="image6_content"
            alt="Send Email"
          />
          <span className="text3_content">Send Email</span>
        </button>
        <button className="button-column2_content" onClick={() => alert("Pressed!")}>
          <img
            src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/4y8rwsnc_expires_30_days.png"
            className="image7_content"
            alt="Describe Img"
          />
          <span className="text3_content">Describe img</span>
        </button>
      </div>
    </div>
  );
}
