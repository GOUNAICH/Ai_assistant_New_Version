import subprocess
import time
import pyautogui
import win32clipboard
from win32con import CF_UNICODETEXT
import psutil
import os

class NotepadHandler:
    def __init__(self, speech_handler):
        self.speech_handler = speech_handler
        self.current_notepad = None
        self.is_dictating = False
        self.max_save_attempts = 3

    async def start_notepad_dictation(self):
        try:
            # Kill ALL existing Notepad processes first
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'].lower() == 'notepad.exe':
                        proc.terminate()
                        proc.wait(timeout=3)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                    pass
            
            time.sleep(0.5)  # Give time for processes to close

            # Create a temporary empty file to force Notepad to open fresh
            temp_file = f"temp_notepad_{time.strftime('%Y%m%d_%H%M%S')}.txt"
            temp_path = os.path.join(os.environ['TEMP'], temp_file)
            
            # Create empty temp file
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write("")
            
            # Open Notepad with the empty temp file
            notepad_path = os.path.join(os.environ['WINDIR'], 'system32', 'notepad.exe')
            self.current_notepad = subprocess.Popen([notepad_path, temp_path])
            
            time.sleep(0.5)  # Give time for Notepad to load
            
            # Clear the temp file content and delete the temp file reference
            pyautogui.hotkey('ctrl', 'a')  # Select all
            time.sleep(0.2)
            pyautogui.press('delete')  # Delete content
            time.sleep(0.2)
            
            # Make sure window is focused
            pyautogui.click(500, 300)
            time.sleep(0.5)
            
            # Clean up temp file
            try:
                os.remove(temp_path)
            except:
                pass  # Don't worry if we can't delete it
            
            self.is_dictating = True
            self.speech_handler.speak("New Notepad is open. What would you like me to write?")

            first_text = await self.speech_handler.listen_command()
            if first_text:
                await self.write_to_notepad(first_text)
            else:
                self.speech_handler.speak("I didn't catch that. Please try again.")
        except Exception as e:
            print(f"Error opening Notepad: {e}")
            self.speech_handler.speak("Sorry, I couldn't open Notepad.")

    async def write_to_notepad(self, text):
        lower_text = text.lower()
        if (lower_text.startswith(('add space', 'new line', 'add line', 'add tab', 'tab', 
                                'delete last character', 'undo character', 'clear notepad',
                                'delete all', 'clear line', 'delete line', 'clear this line',
                                'go back', 'undo', 'go next', 'redo', 'save', 'save file'))):
            return  # Don't write commands as text
            
        try:
            pyautogui.write(text, interval=0.05)
            self.speech_handler.speak("Text written. Continue or say 'save file'.")
        except Exception as e:
            print(f"Error writing to Notepad: {e}")
            self.speech_handler.speak("Sorry, I couldn't write the text.")

    async def save_notepad_file(self):
        attempts = 0
        while attempts < self.max_save_attempts:
            try:
                self.speech_handler.speak("What would you like to name the file?")
                filename = await self.speech_handler.listen_command()
                
                if not filename:
                    attempts += 1
                    if attempts < self.max_save_attempts:
                        self.speech_handler.speak("I didn't catch that. Please try again.")
                        continue
                    else:
                        self.speech_handler.speak("I'm having trouble understanding the filename. Let's use a default name.")
                        filename = f"note_{time.strftime('%Y%m%d_%H%M%S')}"
                
                # Clean filename - remove invalid characters
                filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).strip()
                if not filename:  # If filename is empty after cleaning
                    filename = f"note_{time.strftime('%Y%m%d_%H%M%S')}"
                
                # Open Save As dialog
                pyautogui.hotkey('ctrl', 'shift', 's')  # Save As instead of Save
                time.sleep(1.5)  # Wait for dialog to open
                
                # Clear any existing filename and type new one
                pyautogui.hotkey('ctrl', 'a')  # Select all text in filename field
                time.sleep(0.3)
                pyautogui.write(f"{filename}.txt")
                time.sleep(0.5)
                
                # Press Enter to save
                pyautogui.press('enter')
                time.sleep(1)
                
                # Check if there's a dialog asking to replace file
                # If so, press Enter again to confirm
                try:
                    pyautogui.press('enter')
                    time.sleep(0.5)
                except:
                    pass
                
                self.is_dictating = False
                
                # Close Notepad after saving
                try:
                    pyautogui.hotkey('alt', 'f4')  # Close Notepad
                    time.sleep(0.5)
                    
                    # If there's a save prompt, press 'n' for no (since we just saved)
                    try:
                        pyautogui.press('n')
                    except:
                        pass
                        
                except Exception as close_error:
                    print(f"Error closing Notepad: {close_error}")
                
                # Clean up the process reference
                if self.current_notepad:
                    try:
                        if psutil.pid_exists(self.current_notepad.pid):
                            self.current_notepad.terminate()
                    except:
                        pass
                    self.current_notepad = None
                
                self.speech_handler.speak(f"File saved as {filename}.txt and Notepad closed, Please check your Documents folder.")
                return
                
            except Exception as e:
                print(f"Error saving file (attempt {attempts + 1}): {e}")
                attempts += 1
                if attempts < self.max_save_attempts:
                    self.speech_handler.speak("Sorry, there was an error saving. Let's try again.")
                else:
                    self.speech_handler.speak("I'm having trouble saving the file. Please try manually saving it.")

    async def add_space(self):
        """Add a space in the Notepad."""
        try:
            pyautogui.press('space')
            self.speech_handler.speak("Space added.")
        except Exception as e:
            print(f"Error adding space: {e}")
            self.speech_handler.speak("Sorry, I couldn't add a space.")

    async def add_new_line(self):
        """Add a new line in the Notepad."""
        try:
            pyautogui.press('enter')
            self.speech_handler.speak("New line added.")
        except Exception as e:
            print(f"Error adding new line: {e}")
            self.speech_handler.speak("Sorry, I couldn't add a new line.")

    async def add_tab(self):
        """Add a tab in the Notepad."""
        try:
            pyautogui.press('tab')
            self.speech_handler.speak("Tab added.")
        except Exception as e:
            print(f"Error adding tab: {e}")
            self.speech_handler.speak("Sorry, I couldn't add a tab.")

    async def delete_last_character(self):
        """Delete the last character in the Notepad."""
        try:
            pyautogui.press('backspace')
            self.speech_handler.speak("Last character deleted.")
        except Exception as e:
            print(f"Error deleting character: {e}")
            self.speech_handler.speak("Sorry, I couldn't delete the character.")

    async def clear_notepad(self):
        """Clear all text in the Notepad."""
        try:
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.5)
            pyautogui.press('delete')
            self.speech_handler.speak("Notepad cleared.")
        except Exception as e:
            print(f"Error clearing Notepad: {e}")
            self.speech_handler.speak("Sorry, I couldn't clear the text.")
            
    async def go_back(self):
        """Undo last action and click to deselect."""
        try:
            # Get current mouse position
            x, y = pyautogui.position()
            
            # Perform undo
            pyautogui.hotkey('ctrl', 'z')
            time.sleep(0.3)
            
            # Click to deselect any text
            pyautogui.click(x, y)
            time.sleep(0.1)
            
            self.speech_handler.speak("Undone and ready to edit.")
        except Exception as e:
            print(f"Error with undo: {e}")
            self.speech_handler.speak("Sorry, I couldn't undo properly.")
    
    async def clear_current_line(self):
        """Clear the current line in Notepad by triple-clicking and deleting."""
        try:
            # Bring Notepad to front
            try:
                import win32gui
                hwnd = win32gui.FindWindow("Notepad", None)
                if hwnd:
                    win32gui.SetForegroundWindow(hwnd)
                    time.sleep(0.3)
            except:
                pass

            # Get current mouse position
            current_x, current_y = pyautogui.position()

            # Triple-click to select the line (simulate)
            for _ in range(3):
                pyautogui.click()
                time.sleep(0.1)

            # Press delete
            pyautogui.press('delete')
            time.sleep(0.2)

            # Return mouse to original position
            pyautogui.moveTo(current_x, current_y)

            self.speech_handler.speak("Current line cleared.")

        except Exception as e:
            print(f"Error clearing line: {e}")
            self.speech_handler.speak("Sorry, I couldn't clear the current line. Please make sure Notepad is active.")

    async def go_next(self):
        """Redo last action."""
        try:
            pyautogui.hotkey('ctrl', 'y')
            self.speech_handler.speak("Redone.")
        except Exception as e:
            print(f"Error with redo: {e}")
            self.speech_handler.speak("Sorry, I couldn't redo.")