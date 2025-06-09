import React, { useEffect, useState, useRef } from "react";
import default_assistant from "../../assets/Default_assistant.png";
// Import your emotion images
import happyImg from "../../assets/Hi.png";        // when user says hello/hi
import sadImg from "../../assets/Sad_assistant.png";            // when there's an error
import heartImg from "../../assets/Heart.png";        // when user says thank you/love
import thinkingImg from "../../assets/Happy2.png";  // when processing
import thinkingImgLeft from "../../assets/Left_Eyes_assistant.png";  // when processing
import thinkingImgRight from "../../assets/Right_Eyes_assistant.png";  // when processing
import "../CSS/maincontent.css";

export default function MainContent() {
  const [input1, onChangeInput1] = useState("");
  const [response, setResponse] = useState("Hello, How can I assist you today?");
  const [isListening, setIsListening] = useState(false);
  const [isInitialized, setIsInitialized] = useState(false);
  const [lastUserMessage, setLastUserMessage] = useState("");
  
  // Add state for current assistant image
  const [currentAssistantImg, setCurrentAssistantImg] = useState(default_assistant);
  const [isThinking, setIsThinking] = useState(false);
  
  // Use refs to store timeout IDs for cleanup
  const thinkingAnimationRef = useRef(null);
  const returnToDefaultRef = useRef(null);

  // Function to cycle through thinking images
  const startThinkingAnimation = () => {
    setIsThinking(true);
    setCurrentAssistantImg(thinkingImg);
    
    const cycleThinkingImages = () => {
      // Start with main thinking image for 5 seconds
      setCurrentAssistantImg(thinkingImg);
      
      const timeout1 = setTimeout(() => {
        // Move to right for 3 seconds
        setCurrentAssistantImg(thinkingImgRight);
        
        const timeout2 = setTimeout(() => {
          // Move to left for 3 seconds
          setCurrentAssistantImg(thinkingImgLeft);
          
          const timeout3 = setTimeout(() => {
            // Back to main thinking image and repeat if still thinking
            if (isThinking) {
              cycleThinkingImages();
            }
          }, 3000);
          
          // Store timeout for cleanup
          thinkingAnimationRef.current = timeout3;
        }, 3000);
        
        // Store timeout for cleanup
        thinkingAnimationRef.current = timeout2;
      }, 5000);
      
      // Store timeout for cleanup
      thinkingAnimationRef.current = timeout1;
    };
    
    cycleThinkingImages();
  };

  // Function to stop thinking animation
  const stopThinkingAnimation = () => {
    setIsThinking(false);
    
    // Clear any existing thinking animation timeouts
    if (thinkingAnimationRef.current) {
      clearTimeout(thinkingAnimationRef.current);
      thinkingAnimationRef.current = null;
    }
  };

  // Function to get the right image based on text content
  const getAssistantImage = (text) => {
    const lowerText = text.toLowerCase();
    
    if (lowerText.includes('hello') || lowerText.includes('hi') || lowerText.includes('hey')) {
      return happyImg; // Show happy/waving image
    } else if (lowerText.includes('thank') || lowerText.includes('love') || lowerText.includes('appreciate')) {
      return heartImg; // Show heart eyes image
    } else if (lowerText.includes('sorry') || lowerText.includes('error') || lowerText.includes('problem')) {
      return sadImg; // Show sad image
    } else if (lowerText.includes('thinking') || lowerText.includes('processing') || lowerText.includes('analyzing')) {
      return 'thinking'; // Special case for thinking mode
    } else {
      return default_assistant; // Default image
    }
  };

  // Function to change assistant image with smooth transition
  const changeAssistantImage = (text) => {
    const newImage = getAssistantImage(text);
    
    // Clear any existing return-to-default timeout
    if (returnToDefaultRef.current) {
      clearTimeout(returnToDefaultRef.current);
      returnToDefaultRef.current = null;
    }
    
    if (newImage === 'thinking') {
      // Stop any existing thinking animation and start new one
      stopThinkingAnimation();
      startThinkingAnimation();
    } else {
      // Stop thinking animation if it was running
      stopThinkingAnimation();
      
      setCurrentAssistantImg(newImage);
      
      // Return to default after 2 seconds if not default
      if (newImage !== default_assistant) {
        returnToDefaultRef.current = setTimeout(() => {
          setCurrentAssistantImg(default_assistant);
        }, 2000);
      }
    }
  };

  // Cleanup function
  useEffect(() => {
    return () => {
      // Cleanup timeouts when component unmounts
      if (thinkingAnimationRef.current) {
        clearTimeout(thinkingAnimationRef.current);
      }
      if (returnToDefaultRef.current) {
        clearTimeout(returnToDefaultRef.current);
      }
    };
  }, []);

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
          // Start thinking animation when listening
          stopThinkingAnimation();
          startThinkingAnimation();
        } else if (data && data.trim()) {
          setIsListening(false);
          setResponse(data.trim());
          // Stop thinking animation and change to appropriate image
          stopThinkingAnimation();
          changeAssistantImage(data.trim());
        }
      };

      const handleUserMessage = (message) => {
        setLastUserMessage(`User: ${message}`);
        // Change assistant image based on user message
        changeAssistantImage(message);
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
        {/* Only change: Use currentAssistantImg and add assistant-animate class */}
        <img 
          src={currentAssistantImg} 
          alt="Assistant" 
          className="assistant-animate"
        />
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
            onClick={() => alert("Pressed!")}
          />
          <img
            src="https://storage.googleapis.com/tagjs-prod.appspot.com/v1/8CpHCMTlg6/qorxs7lm_expires_30_days.png"
            className="image4_content"
            alt="Icon 2"
            onClick={() => alert("Pressed!")}
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