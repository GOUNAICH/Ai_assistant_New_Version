import random
from modules.speech import SpeechHandler

class Aboutcrista:
    def __init__(self, speech_handler):
        self.speech_handler = speech_handler
        self.aliases = ["crista", "krista"]  # Just Crista now

        self.greetings = [
            "How can I assist you today?",
            "Ready when you are!",
            "Always here to help!",
            "At your command!",
            "Just say the word!",
            "Let’s get things done!",
            "Hey! What’s up?",
            "Crista is listening!",
            "You called me?",
            "What’s the mission?",
            "Say no more, I’m ready!",
            "How can I make your day easier?",
            "Your assistant is online and ready!"
        ]
        
        self.hello_inputs = [
            "hello", "hi", "hey",
            "hello crista", "hi crista", "hey crista",
        ]
        
        self.features = {
            "document": "Document scanning",
            "phone": "Phone screen control",
            "image": "Image generation and analysis",
            "chat": "AI conversation",
            "email": "Email handling",
            "weather": "Weather updates",
            "notepad": "Voice-controlled text editing",
            "volume": "Volume control",
            "pdf": "PDF reading",
            "applications": "App launching and web search",
            "voice": "Voice command recognition"
        }
        
        self.thank_responses = [
            "You're welcome!",
            "No problem!",
            "Glad to help!",
            "Anytime!",
            "Happy to assist!",
            "With pleasure!"
        ]
        
    def respond(self, command):
        command = command.lower()
        
        # Greetings (hello, hi, etc.)
        if any(word in command for word in self.hello_inputs):
            response = random.choice(self.greetings)
            self.speech_handler.speak(response)
            return

        # Calling Crista by name
        if any(alias in command for alias in self.aliases):
            response = random.choice(self.greetings)
            self.speech_handler.speak(response)
            return

        # Status check
        elif "how are you" in command:
            responses = [
                "I'm functioning perfectly and ready to help!",
                "All systems operational and at your service!",
                "I'm doing great and excited to assist you!",
                "Running smoothly and ready for your commands!"
            ]
            self.speech_handler.speak(random.choice(responses))
        
        # Creator info
        elif "who built you" in command or "who created you" in command or "who made you" in command:
            self.speech_handler.speak(
                "I was developed by Abdeslam Gounaich and Abdelhamid Ben Drif as an advanced virtual assistant."
            )
        
        # Feature list
        elif "what can you do" in command or "your features" in command or "your capabilities" in command:
            self.speech_handler.speak("I'm a versatile virtual assistant. Here are all my features:")
            for feature in self.features.values():
                self.speech_handler.speak(feature)
            self.speech_handler.speak("Would you like to know more about any specific feature?")
        
        # Help
        elif "help me" in command:
            self.speech_handler.speak("You can ask me to perform any task by using natural voice commands.")
        
        # Thanks
        elif "thank you" in command or "thanks" in command:
            self.speech_handler.speak(random.choice(self.thank_responses))
        
        # Unknown command
        else:
            self.speech_handler.speak(
                "I didn't quite catch that. Feel free to ask about my features or give me a specific command."
            )
