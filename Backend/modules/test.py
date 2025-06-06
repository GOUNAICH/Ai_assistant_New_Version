import os
import pyautogui

def test_image_paths():
    print("=" * 50)
    print("IMAGE PATH DEBUGGING")
    print("=" * 50)
    
    # Get current working directory
    current_dir = os.getcwd()
    print(f"Current working directory: {current_dir}")
    print()
    
    # List of possible paths to try
    paths_to_test = [
        "../img/image.png",
        "img/image.png",
        "../../img/image.png", 
        r"C:\Users\Morus\Desktop\Abdo_ai_assistant\img\image.png",
        "../img/files.png"
    ]
    
    print("Testing paths:")
    print("-" * 30)
    
    for path in paths_to_test:
        absolute_path = os.path.abspath(path)
        exists = os.path.exists(path)
        print(f"Path: {path}")
        print(f"Absolute: {absolute_path}")
        print(f"Exists: {exists}")
        
        if exists:
            try:
                # Try to find it on screen
                location = pyautogui.locateCenterOnScreen(path, confidence=0.7)
                if location:
                    print(f"Found on screen at: {location}")
                else:
                    print("File exists but not found on screen")
            except Exception as e:
                print(f"Error testing screen location: {e}")
        print("-" * 30)
    
    print("\nDirectory contents:")
    print("Current directory:", os.listdir("."))
    if os.path.exists(".."):
        print("Parent directory:", os.listdir(".."))
        if os.path.exists("../img"):
            print("../img directory:", os.listdir("../img"))

if __name__ == "__main__":
    test_image_paths()