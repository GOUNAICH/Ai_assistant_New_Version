import os
import shutil
import subprocess
import winreg
from fuzzywuzzy import fuzz

# Enhanced aliases with correct executable names
aliases = {
    # Development Tools
    'vscode': 'Code.exe', 'visual studio code': 'Code.exe', 'vs code': 'Code.exe', 'code': 'Code.exe',
    'codeblocks': 'codeblocks.exe', 'code blocks': 'codeblocks.exe',
    'sublime': 'sublime_text.exe', 'sublime text': 'sublime_text.exe',
    'atom': 'atom.exe', 'notepad++': 'notepad++.exe', 'notepadplusplus': 'notepad++.exe',
    'pycharm': 'pycharm64.exe', 'intellij': 'idea64.exe', 'android studio': 'studio64.exe',
    'postman': 'Postman.exe', 'docker': 'Docker Desktop.exe', 'docker desktop': 'Docker Desktop.exe',
    'git bash': 'git-bash.exe', 'mysql workbench': 'MySQLWorkbench.exe', 'xampp': 'xampp-control.exe',
    'filezilla': 'filezilla.exe', 'putty': 'putty.exe', 'wireshark': 'Wireshark.exe',

    # Browsers
    'chrome': 'chrome.exe', 'google chrome': 'chrome.exe',
    'firefox': 'firefox.exe', 'mozilla firefox': 'firefox.exe',
    'edge': 'msedge.exe', 'microsoft edge': 'msedge.exe', 'safari': 'safari.exe',
    'opera': 'opera.exe', 'brave': 'brave.exe',

    # Communication & Social
    'whatsapp': 'WhatsApp.exe', 'whats app': 'WhatsApp.exe',
    'discord': 'Discord.exe', 'telegram': 'Telegram.exe', 'skype': 'Skype.exe',
    'zoom': 'Zoom.exe', 'teams': 'Teams.exe', 'microsoft teams': 'Teams.exe',
    'slack': 'slack.exe', 'messenger': 'Messenger.exe', 'facebook messenger': 'Messenger.exe',
    'signal': 'Signal.exe', 'viber': 'Viber.exe',

    # Media & Entertainment
    'spotify': 'Spotify.exe', 'vlc': 'vlc.exe', 'vlc player': 'vlc.exe',
    'itunes': 'iTunes.exe', 'netflix': 'Netflix.exe', 'youtube': 'youtube.exe',
    'youtube music': 'YouTube Music.exe', 'amazon music': 'Amazon Music.exe',
    'apple music': 'Apple Music.exe', 'deezer': 'Deezer.exe', 'tidal': 'TIDAL.exe',
    'windows media player': 'wmplayer.exe', 'media player': 'wmplayer.exe',

    # Productivity & Office - Enhanced mapping from second version
    'word': 'WINWORD.EXE', 'microsoft word': 'WINWORD.EXE',
    'excel': 'EXCEL.EXE', 'microsoft excel': 'EXCEL.EXE',
    'powerpoint': 'POWERPNT.EXE', 'microsoft powerpoint': 'POWERPNT.EXE', 'power point': 'POWERPNT.EXE',
    'outlook': 'OUTLOOK.EXE', 'microsoft outlook': 'OUTLOOK.EXE',
    'onenote': 'ONENOTE.EXE', 'microsoft onenote': 'ONENOTE.EXE',
    'access': 'MSACCESS.EXE', 'microsoft access': 'MSACCESS.EXE',
    'publisher': 'MSPUB.EXE', 'microsoft publisher': 'MSPUB.EXE',
    'notion': 'Notion.exe', 'obsidian': 'Obsidian.exe', 'evernote': 'Evernote.exe',
    'trello': 'Trello.exe', 'todoist': 'Todoist.exe',

    # Design & Graphics
    'photoshop': 'Photoshop.exe', 'adobe photoshop': 'Photoshop.exe',
    'illustrator': 'Illustrator.exe', 'adobe illustrator': 'Illustrator.exe',
    'after effects': 'AfterFX.exe', 'adobe after effects': 'AfterFX.exe',
    'premiere': 'Adobe Premiere Pro.exe', 'adobe premiere': 'Adobe Premiere Pro.exe',
    'premiere pro': 'Adobe Premiere Pro.exe', 'indesign': 'InDesign.exe',
    'adobe indesign': 'InDesign.exe', 'lightroom': 'Lightroom.exe',
    'adobe lightroom': 'Lightroom.exe', 'figma': 'Figma.exe',
    'canva': 'Canva.exe', 'gimp': 'gimp.exe', 'blender': 'blender.exe',
    'sketch': 'Sketch.exe', 'coreldraw': 'CorelDRW.exe', 'corel draw': 'CorelDRW.exe',

    # Games
    'steam': 'steam.exe', 'epic games': 'EpicGamesLauncher.exe', 'epic': 'EpicGamesLauncher.exe',
    'origin': 'Origin.exe', 'battle.net': 'Battle.net.exe', 'battlenet': 'Battle.net.exe',
    'uplay': 'upc.exe', 'ubisoft connect': 'upc.exe', 'gog galaxy': 'GalaxyClient.exe',
    'gog': 'GalaxyClient.exe', 'minecraft': 'Minecraft.exe', 'roblox': 'RobloxPlayerLauncher.exe',
    'fortnite': 'FortniteClient-Win64-Shipping.exe',

    # System & Utilities
    'calculator': 'calc.exe', 'calc': 'calc.exe',
    'paint': 'mspaint.exe', 'ms paint': 'mspaint.exe',
    'command prompt': 'cmd.exe', 'cmd': 'cmd.exe',
    'powershell': 'powershell.exe', 'task manager': 'taskmgr.exe', 'taskmgr': 'taskmgr.exe',
    'control panel': 'control.exe', 'file explorer': 'explorer.exe', 'explorer': 'explorer.exe',
    'registry editor': 'regedit.exe', 'regedit': 'regedit.exe',
    'device manager': 'devmgmt.msc', 'services': 'services.msc',
    'msconfig': 'msconfig.exe', 'system configuration': 'msconfig.exe',
    'disk cleanup': 'cleanmgr.exe', 'character map': 'charmap.exe',
    'system information': 'msinfo32.exe',

    # Cloud Storage
    'dropbox': 'Dropbox.exe', 'google drive': 'GoogleDriveFS.exe',
    'onedrive': 'OneDrive.exe', 'microsoft onedrive': 'OneDrive.exe',
    'box': 'Box.exe', 'icloud': 'iCloudDrive.exe',

    # Compression
    'winrar': 'WinRAR.exe', '7zip': '7zFM.exe', '7-zip': '7zFM.exe', 'winzip': 'winzip64.exe',

    # Antivirus
    'windows defender': 'MSASCui.exe', 'defender': 'MSASCui.exe',
    'malwarebytes': 'mbam.exe', 'avast': 'AvastUI.exe', 'avg': 'AVGUI.exe',
    'norton': 'NortonSecurity.exe', 'kaspersky': 'avp.exe', 'mcafee': 'McUICnt.exe',

    # Editors & IDEs
    'vim': 'vim.exe', 'emacs': 'emacs.exe', 'nano': 'nano.exe',
    'brackets': 'Brackets.exe', 'netbeans': 'netbeans64.exe',
    'eclipse': 'eclipse.exe', 'dev-c++': 'devcpp.exe', 'devcpp': 'devcpp.exe',

    # Databases
    'phpmyadmin': 'phpMyAdmin.exe', 'navicat': 'navicat.exe',
    'dbeaver': 'dbeaver.exe', 'pgadmin': 'pgAdmin4.exe',
    'mongodb compass': 'MongoDBCompass.exe', 'compass': 'MongoDBCompass.exe',

    # Virtualization
    'virtualbox': 'VirtualBox.exe', 'vmware': 'vmware.exe', 'vmware workstation': 'vmware.exe',
    'hyper-v': 'virtmgmt.msc',

    # Misc
    'ccleaner': 'CCleaner64.exe', 'teamviewer': 'TeamViewer.exe',
    'anydesk': 'AnyDesk.exe', 'chrome remote desktop': 'remoting_host.exe',
    'utorrent': 'uTorrent.exe', 'bittorrent': 'bittorrent.exe', 'qbittorrent': 'qbittorrent.exe',
    'handbrake': 'HandBrake.exe', 'obs': 'obs64.exe', 'obs studio': 'obs64.exe',
    'audacity': 'audacity.exe', 'kdenlive': 'kdenlive.exe', 'davinci resolve': 'Resolve.exe',
    'unity': 'Unity.exe', 'unreal engine': 'UnrealEditor.exe', 'godot': 'Godot.exe'
}

def find_office_application(app_name):
    """Enhanced Office application finder with multiple registry paths - FROM SECOND VERSION"""
    office_apps = {
        'winword.exe': ['word', 'microsoft word'],
        'excel.exe': ['excel', 'microsoft excel'],
        'powerpnt.exe': ['powerpoint', 'microsoft powerpoint', 'power point'],
        'outlook.exe': ['outlook', 'microsoft outlook'],
        'onenote.exe': ['onenote', 'microsoft onenote'],
        'msaccess.exe': ['access', 'microsoft access'],
        'mspub.exe': ['publisher', 'microsoft publisher']
    }
    
    app_name_lower = app_name.lower()
    target_app = None
    
    # Find which Office app we're looking for
    for exe, names in office_apps.items():
        if app_name_lower in names:
            target_app = exe
            break
    
    if not target_app:
        return None
    
    # Registry paths to check for Office installations
    registry_paths = [
        f"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\{target_app}",
        f"SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\App Paths\\{target_app}",
        "SOFTWARE\\Microsoft\\Office\\ClickToRun\\Configuration",
        "SOFTWARE\\Microsoft\\Office\\16.0\\Common\\InstallRoot",
        "SOFTWARE\\Microsoft\\Office\\15.0\\Common\\InstallRoot",
        "SOFTWARE\\Microsoft\\Office\\14.0\\Common\\InstallRoot"
    ]
    
    for reg_path in registry_paths:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                if "App Paths" in reg_path:
                    path = winreg.QueryValue(key, "")
                    if os.path.exists(path):
                        return path
                else:
                    # For Office installation root paths
                    try:
                        install_path = winreg.QueryValueEx(key, "Path")[0]
                        if install_path:
                            full_path = os.path.join(install_path, target_app.upper())
                            if os.path.exists(full_path):
                                return full_path
                    except FileNotFoundError:
                        continue
        except (WindowsError, OSError):
            continue
    
    return None

def find_vscode():
    """Special handler for VS Code with multiple installation paths - FROM SECOND VERSION"""
    vscode_paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"),
        os.path.expandvars(r"%ProgramFiles%\Microsoft VS Code\Code.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft VS Code\Code.exe"),
        os.path.expandvars(r"%USERPROFILE%\AppData\Local\Programs\Microsoft VS Code\Code.exe")
    ]
    
    for path in vscode_paths:
        if os.path.exists(path):
            return path
    
    # Check registry
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\Code.exe") as key:
            path = winreg.QueryValue(key, "")
            if os.path.exists(path):
                return path
    except (WindowsError, OSError):
        pass
    
    return None

def find_application(app_name):
    """Enhanced application finder - MERGED VERSION"""
    app_name_lower = app_name.lower()
    
    # Check if it's an Office application first (FROM SECOND VERSION)
    office_path = find_office_application(app_name_lower)
    if office_path:
        return office_path
    
    # Special handling for VS Code (FROM SECOND VERSION)
    if app_name_lower in ['vscode', 'visual studio code', 'vs code', 'code']:
        vscode_path = find_vscode()
        if vscode_path:
            return vscode_path
    
    # Check aliases (FROM FIRST VERSION LOGIC)
    app_name = aliases.get(app_name_lower, app_name)
    
    # Try direct path first
    if shutil.which(app_name):
        return app_name

    # Try with .exe if not already present
    if not app_name.lower().endswith('.exe'):
        app_name_exe = app_name + '.exe'
        if shutil.which(app_name_exe):
            return app_name_exe

    # Search common install locations with fuzzy matching (FROM FIRST VERSION)
    search_dirs = [
        r"C:\Program Files",
        r"C:\Program Files (x86)",
        os.path.expandvars(r"%LOCALAPPDATA%\Programs"),
        os.path.expandvars(r"%ProgramFiles%"),
        os.path.expandvars(r"%ProgramW6432%")
    ]

    best_match, best_score = None, 0

    for directory in search_dirs:
        if not os.path.exists(directory):
            continue
            
        try:
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.lower().endswith('.exe'):
                        # Score based on similarity to requested name
                        score = fuzz.ratio(app_name_lower, file.lower())
                        
                        # Bonus points if it's an exact match or contains the name
                        if app_name_lower == file.lower().replace('.exe', ''):
                            score += 50
                        elif app_name_lower in file.lower():
                            score += 20
                            
                        if score > best_score:
                            best_match = os.path.join(root, file)
                            best_score = score
        except (PermissionError, OSError):
            continue

    # If we found a good match, return it
    if best_match and best_score > 75:
        return best_match

    # Search Start Menu shortcuts (FROM FIRST VERSION)
    shortcut_path = find_in_start_menu(app_name_lower)
    if shortcut_path:
        return shortcut_path

    # Try UWP apps via shell execution (FROM FIRST VERSION)
    uwp_path = find_uwp_app(app_name_lower)
    if uwp_path:
        return uwp_path

    return None

def find_in_start_menu(app_name):
    """Search Start Menu for matching shortcuts - FROM FIRST VERSION"""
    start_menu_dirs = [
        os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"),
        os.path.expandvars(r"%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs")
    ]
    
    for directory in start_menu_dirs:
        if not os.path.exists(directory):
            continue
            
        try:
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.lower().endswith('.lnk') and app_name in file.lower():
                        return os.path.join(root, file)
        except (PermissionError, OSError):
            continue
    return None

def find_uwp_app(app_name):
    """Find UWP apps using PowerShell - FROM FIRST VERSION"""
    try:
        result = subprocess.run([
            "powershell", "-Command",
            f"(Get-StartApps | Where-Object {{$_.Name -match '{app_name}'}}).AppId"
        ], capture_output=True, text=True, shell=True)
        
        if result.returncode == 0 and result.stdout.strip():
            return f"shell:AppsFolder\\{result.stdout.strip()}"
    except Exception:
        return None
    return None