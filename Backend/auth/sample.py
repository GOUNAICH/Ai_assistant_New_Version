import cv2
import os
import hashlib
import getpass
import json
import time
import subprocess
import platform
import ctypes
from datetime import datetime

# Setup caméra
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 640)  # largeur de la vidéo
cam.set(4, 480)  # hauteur de la vidéo

# Chemin dynamique vers le fichier cascade
base_dir = os.path.dirname(__file__)
haar_path = os.path.join(base_dir, 'haarcascade_frontalface_default.xml')
samples_dir = os.path.join(base_dir, 'samples')
security_file = os.path.join(base_dir, 'user_security.json')

# Créer le dossier samples s'il n'existe pas
os.makedirs(samples_dir, exist_ok=True)

# Charger le classifieur Haar
detector = cv2.CascadeClassifier(haar_path)

def hash_password(password, salt="face_recognition_salt_2024"):
    """Hash a password using SHA-256 with salt"""
    return hashlib.sha256((password + salt).encode()).hexdigest()

def generate_file_hash(filepath):
    """Generate hash of file content for integrity checking"""
    if not os.path.exists(filepath):
        return None
    
    hash_sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def load_security_data():
    """Load existing security data"""
    if os.path.exists(security_file):
        try:
            with open(security_file, 'r') as f:
                return json.load(f)
        except:
            return {"users": {}, "file_registry": {}}
    return {"users": {}, "file_registry": {}}

def save_security_data(data):
    """Save security data to file"""
    with open(security_file, 'w') as f:
        json.dump(data, f, indent=2)

def register_file(face_id, filename, filepath):
    """Register a file in the security registry"""
    security_data = load_security_data()
    
    if "file_registry" not in security_data:
        security_data["file_registry"] = {}
    
    file_hash = generate_file_hash(filepath)
    security_data["file_registry"][filename] = {
        "user_id": face_id,
        "hash": file_hash,
        "created": datetime.now().isoformat(),
        "path": filepath
    }
    
    save_security_data(security_data)

def verify_file_integrity():
    """Verify integrity of all registered files"""
    security_data = load_security_data()
    file_registry = security_data.get("file_registry", {})
    
    tampered_files = []
    missing_files = []
    
    for filename, file_info in file_registry.items():
        filepath = file_info["path"]
        original_hash = file_info["hash"]
        
        if not os.path.exists(filepath):
            missing_files.append(filename)
        else:
            current_hash = generate_file_hash(filepath)
            if current_hash != original_hash:
                tampered_files.append(filename)
    
    return tampered_files, missing_files

def check_user_exists_in_registry(face_id):
    """Check if user exists in security registry"""
    security_data = load_security_data()
    
    # Check if user exists in users registry
    if face_id in security_data.get("users", {}):
        return True
    
    # Also check if any files are registered for this user
    file_registry = security_data.get("file_registry", {})
    for file_info in file_registry.values():
        if file_info.get("user_id") == face_id:
            return True
    
    return False

def get_user_file_count(face_id):
    """Get count of registered files for user"""
    security_data = load_security_data()
    file_registry = security_data.get("file_registry", {})
    
    count = 0
    for file_info in file_registry.values():
        if file_info.get("user_id") == face_id:
            count += 1
    
    return count

def verify_password(face_id, entered_password):
    """Verify password for existing user"""
    security_data = load_security_data()
    users = security_data.get("users", {})
    
    if face_id in users:
        entered_hash = hash_password(entered_password)
        return entered_hash == users[face_id]["password_hash"]
    return False

def get_first_user_id():
    """Get the first user ID (admin user)"""
    security_data = load_security_data()
    users = security_data.get("users", {})
    
    if not users:
        return None
    
    # Find the user with the earliest creation date
    first_user = None
    earliest_date = None
    
    for user_id, user_info in users.items():
        created = user_info.get("created")
        if created:
            if earliest_date is None or created < earliest_date:
                earliest_date = created
                first_user = user_id
    
    return first_user

def verify_admin_access():
    """Verify admin access using first user's password"""
    first_user = get_first_user_id()
    
    if not first_user:
        return True  # No users exist yet, allow creation
    
    print(f"\n🔐 ADMIN VERIFICATION REQUIRED")
    print(f"To create new users, authenticate with the admin account (User ID: {first_user})")
    
    max_attempts = 3
    for attempt in range(max_attempts):
        password = getpass.getpass(f"Enter password for admin user ID {first_user}: ")
        if verify_password(first_user, password):
            print("✅ Admin authentication successful!")
            return True
        else:
            remaining = max_attempts - attempt - 1
            if remaining > 0:
                print(f"❌ Incorrect password. {remaining} attempts remaining.")
            else:
                print("❌ Admin authentication failed. Cannot create new users.")
                return False
    
    return False

def create_new_password(face_id):
    """Create password for new user"""
    # Check if this is the first user or if admin verification is needed
    security_data = load_security_data()
    existing_users = security_data.get("users", {})
    
    if existing_users:
        # Not the first user, need admin verification
        if not verify_admin_access():
            return False
        
        print(f"\n👤 CREATING NEW USER: {face_id}")
    else:
        print(f"\n👤 CREATING FIRST USER (ADMIN): {face_id}")
        print("This user will have admin privileges to create other users.")
    
    while True:
        password = getpass.getpass("Create a password for this user ID (min 6 characters): ")
        if len(password) < 6:
            print("Password must be at least 6 characters long.")
            continue
        
        confirm_password = getpass.getpass("Confirm password: ")
        if password == confirm_password:
            # Save password hash and user info
            if "users" not in security_data:
                security_data["users"] = {}
            
            security_data["users"][face_id] = {
                "password_hash": hash_password(password),
                "created": datetime.now().isoformat(),
                "last_access": datetime.now().isoformat(),
                "is_admin": len(security_data["users"]) == 0  # First user is admin
            }
            save_security_data(security_data)
            
            if len(security_data["users"]) == 1:
                print("✅ Admin user created successfully!")
            else:
                print("✅ New user created successfully!")
            return True
        else:
            print("Passwords don't match. Please try again.")

def update_last_access(face_id):
    """Update last access time for user"""
    security_data = load_security_data()
    if face_id in security_data.get("users", {}):
        security_data["users"][face_id]["last_access"] = datetime.now().isoformat()
        save_security_data(security_data)

def authenticate_user(face_id):
    """Handle user authentication with integrity checks"""
    
    # First, check file integrity
    tampered_files, missing_files = verify_file_integrity()
    
    if tampered_files or missing_files:
        print("⚠️  SECURITY ALERT: File integrity check failed!")
        if missing_files:
            print(f"Missing files detected: {len(missing_files)} files")
        if tampered_files:
            print(f"Tampered files detected: {len(tampered_files)} files")
        
        print("This could indicate:")
        print("- Manual deletion/modification of sample files")
        print("- Unauthorized access to the samples directory")
        print("- System corruption")
        
        # For existing users, require authentication to proceed
        if check_user_exists_in_registry(face_id):
            print(f"\nUser ID {face_id} exists but samples are compromised.")
            print("Authentication required to rebuild samples...")
            
            max_attempts = 3
            for attempt in range(max_attempts):
                password = getpass.getpass(f"Enter password for user ID {face_id}: ")
                if verify_password(face_id, password):
                    print("Authentication successful!")
                    update_last_access(face_id)
                    
                    # Clean up registry for this user due to integrity issues
                    cleanup_user_registry(face_id)
                    print("Sample registry cleaned due to integrity issues.")
                    return 'R'  # Force rebuild
                else:
                    remaining = max_attempts - attempt - 1
                    if remaining > 0:
                        print(f"Incorrect password. {remaining} attempts remaining.")
                    else:
                        print("❌ Maximum attempts exceeded. Access denied.")
                        return None
        else:
            print("No valid user found. Starting as new user...")
            return 'N'
    
    # Normal flow if integrity is good
    if check_user_exists_in_registry(face_id):
        sample_count = get_user_file_count(face_id)
        print(f"User ID {face_id} found with {sample_count} registered samples")
        print("Authentication required to proceed.")
        
        max_attempts = 3
        for attempt in range(max_attempts):
            password = getpass.getpass(f"Enter password for user ID {face_id}: ")
            if verify_password(face_id, password):
                print("Authentication successful!")
                update_last_access(face_id)
                
                # Ask what to do with existing samples
                while True:
                    choice = input("Do you want to (R)eplace existing samples or (A)dd more samples? [R/A]: ").upper().strip()
                    if choice in ['R', 'A']:
                        return choice
                    print("Please enter 'R' for replace or 'A' for add more.")
            else:
                remaining = max_attempts - attempt - 1
                if remaining > 0:
                    print(f"Incorrect password. {remaining} attempts remaining.")
                else:
                    print("❌ Maximum attempts exceeded. Access denied.")
                    return None
        return None
    else:
        print(f"New user ID {face_id}. Creating security profile...")
        if create_new_password(face_id):
            return 'N'  # New user
        return None

def cleanup_user_registry(face_id):
    """Remove all registry entries for a user"""
    security_data = load_security_data()
    file_registry = security_data.get("file_registry", {})
    
    # Remove files belonging to this user from registry
    files_to_remove = []
    for filename, file_info in file_registry.items():
        if file_info.get("user_id") == face_id:
            files_to_remove.append(filename)
    
    for filename in files_to_remove:
        del file_registry[filename]
    
    save_security_data(security_data)

def delete_existing_samples(face_id):
    """Delete existing samples for the user and clean registry"""
    deleted_count = 0
    
    # Delete physical files
    for filename in os.listdir(samples_dir):
        if filename.startswith(f"face.{face_id}.") and filename.endswith('.jpg'):
            file_path = os.path.join(samples_dir, filename)
            try:
                os.remove(file_path)
                deleted_count += 1
            except:
                pass
    
    # Clean up registry
    cleanup_user_registry(face_id)
    
    print(f"Deleted {deleted_count} existing samples and cleaned registry.")

def get_next_sample_number(face_id):
    """Get the next sample number for continuing sample collection"""
    security_data = load_security_data()
    file_registry = security_data.get("file_registry", {})
    
    max_num = 0
    for filename, file_info in file_registry.items():
        if file_info.get("user_id") == face_id:
            try:
                # Extract number from filename like "face.1.123.jpg"
                parts = filename.split('.')
                if len(parts) >= 3:
                    num = int(parts[2])
                    max_num = max(max_num, num)
            except:
                continue
    
    return max_num

def show_user_management_menu():
    """Show user management options"""
    print("\n" + "="*50)
    print("🏠 USER MANAGEMENT SYSTEM")
    print("="*50)
    
    security_data = load_security_data()
    users = security_data.get("users", {})
    
    if users:
        print("📋 EXISTING USERS:")
        for user_id, user_info in users.items():
            created = user_info.get("created", "Unknown")
            last_access = user_info.get("last_access", "Never")
            is_admin = user_info.get("is_admin", False)
            admin_tag = " [ADMIN]" if is_admin else ""
            
            print(f"   • User ID: {user_id}{admin_tag}")
            print(f"     Created: {created[:19] if created != 'Unknown' else 'Unknown'}")
            print(f"     Last Access: {last_access[:19] if last_access != 'Never' else 'Never'}")
            print()
    else:
        print("👤 No users found. First user will become admin.")
    
    print("OPTIONS:")
    print("1. Create samples for existing user")
    print("2. Create new user")
    print("3. Exit")
    print("="*50)

# Main execution starts here
show_user_management_menu()

while True:
    choice = input("\nSelect an option (1-3): ").strip()
    
    if choice == "1":
        # Existing user flow
        while True:
            face_id = input("Enter the user ID: ").strip()
            if face_id.isdigit():
                if check_user_exists_in_registry(face_id):
                    break
                else:
                    print(f"❌ User ID {face_id} does not exist.")
                    retry = input("Try again? (y/n): ").lower().strip()
                    if retry != 'y':
                        face_id = None
                        break
            else:
                print("Invalid input. Please enter a numeric ID.")
        
        if face_id:
            # Authenticate existing user
            auth_result = authenticate_user(face_id)
            if auth_result is not None:
                break
        continue
    
    elif choice == "2":
        # New user creation
        security_data = load_security_data()
        existing_users = security_data.get("users", {})
        
        if existing_users:
            # Need admin verification
            if not verify_admin_access():
                print("Cannot create new user without admin authentication.")
                continue
        
        while True:
            face_id = input("Enter a new numeric user ID: ").strip()
            if face_id.isdigit():
                if not check_user_exists_in_registry(face_id):
                    break
                else:
                    print(f"❌ User ID {face_id} already exists.")
            else:
                print("Invalid input. Please enter a numeric ID.")
        
        if create_new_password(face_id):
            auth_result = 'N'  # New user
            break
        continue
    
    elif choice == "3":
        print("👋 Goodbye!")
        cam.release()
        cv2.destroyAllWindows()
        exit()
    
    else:
        print("❌ Invalid choice. Please select 1, 2, or 3.")

# Remove the old user input section
# while True:
#     face_id = input("Enter a numeric user ID here: ").strip()
#     if face_id.isdigit():
#         break
#     else:
#         print("Invalid input. Please enter a numeric ID (e.g., 1, 2, 3...)")

# # Authenticate user
# auth_result = authenticate_user(face_id)
# if auth_result is None:
#     print("Authentication failed. Exiting...")
#     cam.release()
#     cv2.destroyAllWindows()
#     exit()

# Handle existing samples based on user choice
if auth_result == 'R':
    delete_existing_samples(face_id)
    print("Existing samples deleted. Starting fresh...")
    count = 0
elif auth_result == 'A':
    print("Adding more samples to existing collection...")
    count = get_next_sample_number(face_id)
    print(f"Continuing from sample {count}...")
else:  # New user
    count = 0

print("Taking samples, look at the camera .......")
print("Press ESC to stop early or wait for 100 samples")
print("🔒 All samples are being registered with security hashes...")

while True:
    ret, img = cam.read()
    if not ret:
        print("Failed to grab frame")
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        # Show count and security status on image
        cv2.putText(img, f'Samples: {count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img, 'SECURED', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Enregistrer l'image
        filename = f"face.{face_id}.{count}.jpg"
        face_path = os.path.join(samples_dir, filename)
        cv2.imwrite(face_path, gray[y:y+h, x:x+w])
        
        # Register the file in security system
        register_file(face_id, filename, face_path)

        cv2.imshow('Face Sample Collection - SECURED', img)

    k = cv2.waitKey(100) & 0xff
    if k == 27:  # touche ESC
        print("Stopped by user.")
        break
    elif count >= 100:
        print("Reached maximum samples (100).")
        break

print(f"Sample collection completed. Total samples taken: {count}")
print("🔒 All samples are password protected and registered with integrity hashes.")
print("⚠️  Manual file deletion/modification will be detected on next run!")
cam.release()
cv2.destroyAllWindows()