import sys
import asyncio
import random
import re
import PyPDF2
from PyQt6.QtWidgets import QApplication, QFileDialog
from modules.speech import SpeechHandler
import webbrowser
from modules.utils import find_application

class InteractivePDFCompanion:
    def __init__(self, file_path=None):
        self.speaker = SpeechHandler()
        self.file_path = file_path if file_path else self.select_pdf_file()
        self.pdf_reader = None
        self.total_pages = 0
        self.book = None
        self.current_page = 0
        self.current_paragraph = 0
        self.structure = []
        
        self.reactions = [
            "Ready for more?",
            "Shall we continue?",
            "Would you like to hear that again?",
            "What do you think so far?",
        ]

    def select_pdf_file(self):
        self.speaker.speak("Please select a PDF to read.")
        app = QApplication.instance() or QApplication(sys.argv)
        file_path, _ = QFileDialog.getOpenFileName(None, "Select a PDF file", "", "PDF Files (*.pdf)")
        
        if not file_path:
            self.speaker.speak("No file selected. Goodbye!")
            sys.exit()
        
        self.speaker.speak("Great choice!")
        return file_path

    def parse_page_structure(self, text):
        lines = text.split('\n')
        structure = []
        current_paragraph = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Better title detection
            if len(line) < 100 and (line.isupper() or (line.istitle() and not line.endswith('.'))):
                if current_paragraph:
                    structure.append(('paragraph', ' '.join(current_paragraph)))
                    current_paragraph = []
                structure.append(('title', line))
            else:
                current_paragraph.append(line)
                
                # End paragraph on sentence endings or when line is long enough
                if line.endswith('.') and len(' '.join(current_paragraph)) > 50:
                    structure.append(('paragraph', ' '.join(current_paragraph)))
                    current_paragraph = []
                    
        if current_paragraph:
            structure.append(('paragraph', ' '.join(current_paragraph)))
        
        # If no structure found, treat whole text as one paragraph
        if not structure and text.strip():
            structure.append(('paragraph', text.strip()))
        
        return structure

    def open_pdf(self):
        try:
            self.speaker.speak("Opening PDF, please wait...")
            
            # Load the PDF for reading first
            self.book = open(self.file_path, "rb")
            self.pdf_reader = PyPDF2.PdfReader(self.book)
            self.total_pages = len(self.pdf_reader.pages)
            
            # Open in browser
            chrome_path = find_application("chrome")
            if chrome_path:
                webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path))
                webbrowser.get("chrome").open(self.file_path)
            else:
                self.speaker.speak("Google Chrome not found. Opening in the default browser instead.")
                webbrowser.open(self.file_path)

            self.speaker.speak(f"PDF loaded successfully. {self.total_pages} pages available.")
            return True

        except Exception as e:
            self.speaker.speak(f"Error opening PDF: {str(e)}")
            return False

    def load_page(self, page_num):
        try:
            if 0 <= page_num < self.total_pages:
                self.current_page = page_num
                self.speaker.speak(f"Loading page {self.current_page + 1}")
                page = self.pdf_reader.pages[page_num]
                text = page.extract_text() or "No readable text on this page."
                self.structure = self.parse_page_structure(text)
                self.current_paragraph = 0
                
                if not self.structure:
                    self.speaker.speak("This page appears to be empty or unreadable.")
                    return False
                    
                return True
            else:
                self.speaker.speak(f"Invalid page number. Please choose between 1 and {self.total_pages}.")
                return False
        except Exception as e:
            self.speaker.speak(f"Error loading page: {str(e)}")
            return False
    
    async def ask_page_number(self):
        max_attempts = 3
        attempt = 0
        
        while attempt < max_attempts:
            try:
                self.speaker.speak(f"Which page would you like me to read? Please say a number from 1 to {self.total_pages}.")
                
                # Add a small delay before listening
                await asyncio.sleep(1)
                
                response = await self.speaker.listen_command()
                
                if response:
                    response = response.strip()
                    print(f"Debug: Received response: '{response}'")  # Debug line
                    
                    # Try to extract number from response
                    numbers = re.findall(r'\d+', response)
                    if numbers:
                        page_num = int(numbers[0])
                        if 1 <= page_num <= self.total_pages:
                            self.speaker.speak(f"Great! Going to page {page_num}.")
                            return page_num - 1
                        else:
                            self.speaker.speak(f"Page {page_num} is out of range. Please choose between 1 and {self.total_pages}.")
                    else:
                        self.speaker.speak("I didn't hear a number. Please say a page number clearly.")
                else:
                    self.speaker.speak("I didn't catch that. Please try again.")
                    
            except Exception as e:
                self.speaker.speak("Sorry, there was an error. Let me try again.")
                print(f"Debug: Error in ask_page_number: {e}")
                
            attempt += 1
            await asyncio.sleep(0.5)  # Small delay between attempts
        
        # If all attempts failed, default to page 1
        self.speaker.speak("Let's start with page 1.")
        return 0

    async def handle_command(self):
        max_attempts = 2
        attempt = 0
        
        while attempt < max_attempts:
            try:
                self.speaker.speak("Say: 'continue', 'repeat', 'next page', 'previous page', 'go to page X', or 'stop'")
                await asyncio.sleep(1)
                
                command = await self.speaker.listen_command()
                
                if command:
                    command = command.lower().strip()
                    print(f"Debug: Command received: '{command}'")  # Debug line
                    
                    if any(word in command for word in ['stop', 'quit', 'exit', 'end']):
                        return False
                    elif any(word in command for word in ['repeat', 'again']):
                        return 'repeat'
                    elif 'next page' in command or 'next' in command:
                        if self.current_page < self.total_pages - 1:
                            self.current_page += 1
                            if self.load_page(self.current_page):
                                return 'next_page'
                            else:
                                return 'repeat'
                        else:
                            self.speaker.speak("This is the last page.")
                            return 'repeat'
                    elif 'previous page' in command or 'back' in command or 'prev' in command:
                        if self.current_page > 0:
                            self.current_page -= 1
                            if self.load_page(self.current_page):
                                return 'previous_page'
                            else:
                                return 'repeat'
                        else:
                            self.speaker.speak("This is the first page.")
                            return 'repeat'
                    elif 'go to page' in command or 'page' in command:
                        numbers = re.findall(r'\d+', command)
                        if numbers:
                            page_number = int(numbers[0]) - 1
                            if 0 <= page_number < self.total_pages:
                                self.current_page = page_number
                                if self.load_page(self.current_page):
                                    return 'go_to_page'
                                else:
                                    return 'repeat'
                            else:
                                self.speaker.speak(f"Invalid page number. Choose between 1 and {self.total_pages}.")
                                return 'repeat'
                        else:
                            self.speaker.speak("Please specify a page number.")
                            return 'repeat'
                    elif any(word in command for word in ['continue', 'next', 'go on', 'more']):
                        if self.current_paragraph < len(self.structure) - 1:
                            self.current_paragraph += 1
                            return 'continue'
                        else:
                            self.speaker.speak("End of page reached. Say 'next page' to continue or another command.")
                            return 'repeat'
                    else:
                        self.speaker.speak("I didn't understand that command. Let me repeat the options.")
                        return 'repeat'
                else:
                    self.speaker.speak("I didn't hear you. Let me try again.")
                    
            except Exception as e:
                self.speaker.speak("Sorry, there was an error processing your command.")
                print(f"Debug: Error in handle_command: {e}")
                
            attempt += 1
            await asyncio.sleep(0.5)
        
        # Default to repeat if all attempts failed
        return 'repeat'
    
    async def read_current_section(self):
        try:
            if 0 <= self.current_paragraph < len(self.structure):
                section_type, content = self.structure[self.current_paragraph]
                
                if section_type == 'title':
                    self.speaker.speak(f"Title: {content}")
                else:
                    # Split long paragraphs into smaller chunks
                    if len(content) > 500:
                        sentences = content.split('. ')
                        chunk_size = 3  # Read 3 sentences at a time
                        for i in range(0, len(sentences), chunk_size):
                            chunk = '. '.join(sentences[i:i+chunk_size])
                            if not chunk.endswith('.'):
                                chunk += '.'
                            self.speaker.speak(chunk)
                            await asyncio.sleep(0.5)  # Small pause between chunks
                    else:
                        self.speaker.speak(content)
                
                # Only add reaction if not at the end of page
                if self.current_paragraph < len(self.structure) - 1:
                    self.speaker.speak(random.choice(self.reactions))
                else:
                    self.speaker.speak("End of page reached.")
            else:
                self.speaker.speak("No content available for this section.")
                
        except Exception as e:
            self.speaker.speak("Error reading current section.")
            print(f"Debug: Error in read_current_section: {e}")
    
    async def start_reading(self):
        try:
            if not self.open_pdf():
                return
            
            await asyncio.sleep(2)  # Allow PDF to load in browser
            page_num = await self.ask_page_number()
            
            if not self.load_page(page_num):
                self.speaker.speak("Failed to load the page. Exiting.")
                return
            
            self.speaker.speak("Starting to read. You can interrupt me anytime with commands.")
            
            while True:
                await self.read_current_section()
                command = await self.handle_command()
                
                if command is False:
                    self.speaker.speak("Thanks for reading with me! Goodbye!")
                    break
                elif command == 'next_page':
                    self.speaker.speak(f"Now on page {self.current_page + 1}")
                elif command == 'previous_page':
                    self.speaker.speak(f"Back to page {self.current_page + 1}")
                elif command == 'go_to_page':
                    self.speaker.speak(f"Now on page {self.current_page + 1}")
                elif command == 'continue':
                    continue  # Just continue to next section
                # For 'repeat', we just continue the loop
                
                await asyncio.sleep(0.3)  # Small delay between operations
        
        except Exception as e:
            self.speaker.speak("An error occurred during reading.")
            print(f"Debug: Error in start_reading: {e}")
        finally:
            if self.book:
                self.book.close()
