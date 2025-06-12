import subprocess
import os

class PhoneDisplayHandler:
    def __init__(self, speech_handler):
        self.speech_handler = speech_handler
        self.scrcpy_process = None
        self.is_phone_displayed = False

    async def display_phone(self):
        if self.is_phone_displayed:
            self.speech_handler.speak("Your phone screen is already being displayed.")
            return

        try:
            # Go one level up from current file, then into Display_Phone/scrcpy.exe
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            scrcpy_path = os.path.join(base_dir, "Display_Phone", "scrcpy.exe")

            self.scrcpy_process = subprocess.Popen(scrcpy_path, shell=True)
            self.speech_handler.speak("Displaying your phone screen.")
            self.is_phone_displayed = True
        except Exception as e:
            print(f"Error starting scrcpy: {e}")
            self.speech_handler.speak("Failed to display your phone screen.")

    def stop_display(self):
        try:
            if self.is_phone_displayed and self.scrcpy_process:
                subprocess.run(['taskkill', '/F', '/IM', 'scrcpy.exe'],
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
                self.scrcpy_process = None
                self.is_phone_displayed = False
                self.speech_handler.speak("Stopped displaying phone screen.")
            else:
                self.speech_handler.speak("Phone screen is not being displayed.")
        except Exception as e:
            print(f"Error stopping display: {e}")
            self.speech_handler.speak("Error occurred while trying to stop the display.")