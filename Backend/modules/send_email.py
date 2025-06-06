import pyautogui
import time
import webbrowser
from modules.speech import SpeechHandler
import os
import sys

class SendEmail:
    def __init__(self, speech_handler: SpeechHandler):
        self.speech_handler = speech_handler

    def get_image_path(self, relative_path):
        """Helper method to get correct image path"""
        try:
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            return os.path.join(base_path, relative_path)
        except Exception:
            return relative_path

    def open_gmail(self):
        webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
        self.speech_handler.speak("Opening Gmail. Please wait...")
        time.sleep(3)  # Increased wait time for page load

    def click_new_message(self):
        self.speech_handler.speak("Clicking on 'New Message'.")
        time.sleep(1)  # Wait for Gmail to load

        try:
            img_path = self.get_image_path("../img/image.png")
            if not os.path.exists(img_path):
                self.speech_handler.speak("Error: 'New Message' button image not found.")
                return False
            
            for attempt in range(5):
                button_location = pyautogui.locateCenterOnScreen(img_path, confidence=0.7)
                if button_location:
                    pyautogui.moveTo(button_location, duration=0.3)
                    pyautogui.click()
                    self.speech_handler.speak("New message window opened.")
                    return True
                time.sleep(1)
            
            self.speech_handler.speak("Could not find 'New Message'. Try clicking manually.")
            return False

        except Exception as e:
            self.speech_handler.speak(f"Error clicking 'New Message': {str(e)}")
            return False

    async def get_voice_input(self, prompt, retries=2):
        for attempt in range(retries):
            self.speech_handler.speak(prompt)
            time.sleep(1)

            try:
                response = await self.speech_handler.listen_command()
                if response:
                    return response.strip().lower()
            except Exception as e:
                self.speech_handler.speak(f"Error processing speech: {e}")
        
        self.speech_handler.speak("I didn't hear you. Let's try again.")
        return ""

    async def type_recipient(self):
        recipient = await self.get_voice_input("Who do you want to send the email to?")   
        if recipient:
            recipient = recipient.replace(" ", "")  # Remove spaces
            pyautogui.write(recipient + "@gmail.com")
            pyautogui.press("tab")
            self.speech_handler.speak(f"Recipient set to {recipient}.")
            time.sleep(1)

    async def type_subject(self):
        subject = await self.get_voice_input("What is the subject of your email?") 
        if subject:
            pyautogui.write(subject)
            pyautogui.press("tab")
            self.speech_handler.speak(f"Subject set to {subject}.")
            time.sleep(1)

    async def type_message(self):
        message = await self.get_voice_input("What is the message?") 
        if message:
            pyautogui.write(message)
            self.speech_handler.speak("Message written")
            time.sleep(1)
        
    async def handle_attachments(self):
        """Handles file attachment process"""
        try:
            self.speech_handler.speak("Looking for the attach button.")
            img_path = self.get_image_path("../img/files.png")
            
            if not os.path.exists(img_path):
                self.speech_handler.speak("Error: Attachment button image not found.")
                return

            found = False
            for attempt in range(5):
                print(f"Debug: Attempt {attempt + 1} to locate attachment button...")
                attach_btn = pyautogui.locateCenterOnScreen(img_path, confidence=0.85)
                if attach_btn:
                    pyautogui.moveTo(attach_btn, duration=0.3)
                    pyautogui.click()
                    self.speech_handler.speak("Please select your file. I'll wait 20 seconds.")
                    time.sleep(20)
                    self.speech_handler.speak("File attached successfully.")
                    found = True
                    break
                else:
                    print("Debug: Attachment button not found this attempt.")
                time.sleep(1)

            if not found:
                # Fallback to keyboard shortcut Shift + A
                self.speech_handler.speak("Could not find the attach button. Using keyboard shortcut to open attachment dialog.")
                pyautogui.hotkey("shift", "a")
                time.sleep(2)
                self.speech_handler.speak("Please select your file. I'll wait 20 seconds.")
                time.sleep(20)
                self.speech_handler.speak("File attached successfully via shortcut.")

        except Exception as e:
            self.speech_handler.speak(f"Attachment error: {str(e)}")
            print(f"Exception in handle_attachments: {e}")

    async def ask_attachments(self):
        response = await self.get_voice_input("Do you want to attach any files or images? Say yes or no.")
        
        if response in ["yes", "yeah", "sure", "okay", "alright"]:
            await self.handle_attachments()
        elif response in ["no", "nah", "skip"]:
            self.speech_handler.speak("Skipping attachments.")
        else:
            self.speech_handler.speak("I didn't understand. Please say yes or no.")
            await self.ask_attachments()
  
    async def send_email(self):
        confirmation = await self.get_voice_input("Say 'yes' to send the email or 'no' to cancel.")
        if "yes" in confirmation.lower():
            pyautogui.hotkey("ctrl", "enter")
            time.sleep(1)
            self.speech_handler.speak("Email sent successfully.")
        else:
            self.speech_handler.speak("Email cancelled.")

    async def handle_send_email(self):
        self.open_gmail()
        
        success = self.click_new_message()
        if not success:
            self.speech_handler.speak("Email process cancelled because 'New Message' could not be found.")
            return  

        await self.type_recipient()
        await self.type_subject()
        await self.type_message()
        await self.ask_attachments()
        await self.send_email()
