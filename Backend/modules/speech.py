import speech_recognition as sr
import pyttsx3
import sys

class SpeechHandler:
    def __init__(self):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)
        self.recognizer = sr.Recognizer()

    def speak(self, text):
        print(f"Assistant: {text}", flush=True)
        self.engine.say(text)
        self.engine.runAndWait()

    def stop_speaking(self):
            """Stop speaking immediately."""
            self.engine.stop()

    async def listen_command(self):
        print(f"Listening...", flush=True)
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            try:
                command = self.recognizer.recognize_google(audio)
                return command.lower()
            except sr.UnknownValueError:
                return None
            except Exception as e:
                print(f"Error: {e}", flush=True)
                return None
