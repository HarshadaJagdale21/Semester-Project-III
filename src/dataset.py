# dataset.py
# Ready-to-use dataset for Jarvis AI Assistant
# Format: "command_name": "path_to_app_or_folder"

DATASET = {
    # ---------------- 1. System Utilities ----------------
    "notepad": "C:\\Windows\\System32\\notepad.exe",
    "calculator": "C:\\Windows\\System32\\calc.exe",
    "paint": "C:\\Windows\\System32\\mspaint.exe",
    "cmd": "C:\\Windows\\System32\\cmd.exe",
    "task manager": "C:\\Windows\\System32\\Taskmgr.exe",
    "file explorer": "C:\\Windows\\explorer.exe",
    "control panel": "C:\\Windows\\System32\\control.exe",
    "registry editor": "C:\\Windows\\System32\\regedit.exe",
    "windows settings": "C:\\Windows\\System32\\StartMenuExperienceHost.exe",

    # ---------------- 2. Microsoft Office ----------------
    "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
    "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
    "powerpoint": "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE",
    "onenote": "C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.EXE",
    "outlook": "C:\\Program Files\\Microsoft Office\\root\\Office16\\OUTLOOK.EXE",
    "access": "C:\\Program Files\\Microsoft Office\\root\\Office16\\MSACCESS.EXE",
    "publisher": "C:\\Program Files\\Microsoft Office\\root\\Office16\\MSPUB.EXE",

    # ---------------- 3. Browsers ----------------
    "google chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "microsoft edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "mozilla firefox": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
    "opera": "C:\\Program Files\\Opera\\launcher.exe",
    "brave": "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",

    # ---------------- 4. Communication Apps ----------------
    "whatsapp": "C:\\Users\\%USERNAME%\\AppData\\Local\\WhatsApp\\WhatsApp.exe",
    "teams": "C:\\Users\\%USERNAME%\\AppData\\Local\\Microsoft\\Teams\\Update.exe",
    "zoom": "C:\\Users\\%USERNAME%\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe",
    "slack": "C:\\Users\\%USERNAME%\\AppData\\Local\\slack\\slack.exe",
    "skype": "C:\\Program Files (x86)\\Microsoft\\Skype for Desktop\\Skype.exe",
    "telegram": "C:\\Users\\%USERNAME%\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe",

    # ---------------- 5. Code Editors / IDEs ----------------
    "vs code": "C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
    "pycharm": "C:\\Program Files\\JetBrains\\PyCharm Community Edition 2023.1.2\\bin\\pycharm64.exe",
    "sublime text": "C:\\Program Files\\Sublime Text 3\\sublime_text.exe",
    "atom": "C:\\Users\\%USERNAME%\\AppData\\Local\\atom\\atom.exe",
    "eclipse": "C:\\Program Files\\eclipse\\eclipse.exe",
    "visual studio": "C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\Common7\\IDE\\devenv.exe",
    "intellij idea": "C:\\Program Files\\JetBrains\\IntelliJ IDEA Community Edition 2023.1.2\\bin\\idea64.exe",

    # ---------------- 6. Media & Entertainment ----------------
    "vlc": "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",
    "spotify": "C:\\Users\\%USERNAME%\\AppData\\Roaming\\Spotify\\Spotify.exe",
    "windows media player": "C:\\Program Files\\Windows Media Player\\wmplayer.exe",
    "movies & tv": "C:\\Program Files\\WindowsApps\\Microsoft.ZuneVideo_*\\Video.UI.exe",
    "photos": "C:\\Windows\\System32\\PhotosApp.exe",
    "groove music": "C:\\Program Files\\WindowsApps\\Microsoft.ZuneMusic_*\\Music.UI.exe",
    "camera": "C:\\Windows\\System32\\WindowsCamera.exe",

    # ---------------- 7. Common Folders ----------------
    "desktop": "C:\\Users\\%USERNAME%\\Desktop",
    "documents": "C:\\Users\\%USERNAME%\\Documents",
    "downloads": "C:\\Users\\%USERNAME%\\Downloads",
    "pictures": "C:\\Users\\%USERNAME%\\Pictures",
    "music": "C:\\Users\\%USERNAME%\\Music",
    "videos": "C:\\Users\\%USERNAME%\\Videos",
    "favorites": "C:\\Users\\%USERNAME%\\Favorites",
    "public folder": "C:\\Users\\Public",

    # ---------------- 8. Installed Games (Optional) ----------------
    "steam": "C:\\Program Files (x86)\\Steam\\Steam.exe",
    "epic games launcher": "C:\\Program Files\\Epic Games\\Launcher\\Launcher.exe",
    "minecraft": "C:\\Program Files (x86)\\Minecraft Launcher\\MinecraftLauncher.exe",
    "roblox": "C:\\Users\\%USERNAME%\\AppData\\Local\\Roblox\\RobloxPlayerLauncher.exe",
    "valorant": "C:\\Riot Games\\VALORANT\\live\\VALORANT.exe",
    "league of legends": "C:\\Riot Games\\League of Legends\\LeagueClient.exe",

    # ---------------- 9. System Folders / Drives ----------------
    "c drive": "C:\\",
    "d drive": "D:\\",
    "program files": "C:\\Program Files",
    "program files x86": "C:\\Program Files (x86)",
    "appdata local": "C:\\Users\\%USERNAME%\\AppData\\Local",
    "appdata roaming": "C:\\Users\\%USERNAME%\\AppData\\Roaming",

    # ---------------- 10. File Types ----------------
    "word document": "C:\\Users\\%USERNAME%\\Documents\\example.docx",
    "excel file": "C:\\Users\\%USERNAME%\\Documents\\example.xlsx",
    "powerpoint file": "C:\\Users\\%USERNAME%\\Documents\\example.pptx",
    "pdf": "C:\\Users\\%USERNAME%\\Documents\\example.pdf",
    "image": "C:\\Users\\%USERNAME%\\Pictures\\example.jpg",
    "music file": "C:\\Users\\%USERNAME%\\Music\\example.mp3",
    "video file": "C:\\Users\\%USERNAME%\\Videos\\example.mp4",
    "text file": "C:\\Users\\%USERNAME%\\Documents\\example.txt",

    # ---------------- 11. Common Apps Shortcuts ----------------
    "vs code shortcut": "C:\\Users\\%USERNAME%\\Desktop\\VS Code.lnk",
    "chrome shortcut": "C:\\Users\\%USERNAME%\\Desktop\\Chrome.lnk",
    "spotify shortcut": "C:\\Users\\%USERNAME%\\Desktop\\Spotify.lnk",
    "zoom shortcut": "C:\\Users\\%USERNAME%\\Desktop\\Zoom.lnk",
    "whatsapp shortcut": "C:\\Users\\%USERNAME%\\Desktop\\WhatsApp.lnk",
    "edge shortcut": "C:\\Users\\%USERNAME%\\Desktop\\Edge.lnk",
    "notepad shortcut": "C:\\Users\\%USERNAME%\\Desktop\\Notepad.lnk",
    "calculator shortcut": "C:\\Users\\%USERNAME%\\Desktop\\Calculator.lnk",
    "paint shortcut": "C:\\Users\\%USERNAME%\\Desktop\\Paint.lnk",
    "vlc shortcut": "C:\\Users\\%USERNAME%\\Desktop\\VLC.lnk",

    # ---------------- 12. Additional Optional Apps ----------------
    "adobe reader": "C:\\Program Files (x86)\\Adobe\\Acrobat Reader DC\\Reader\\AcroRd32.exe",
    "adobe photoshop": "C:\\Program Files\\Adobe\\Adobe Photoshop 2023\\Photoshop.exe",
    "adobe illustrator": "C:\\Program Files\\Adobe\\Adobe Illustrator 2023\\Support Files\\Contents\\Windows\\Illustrator.exe",
    "filezilla": "C:\\Program Files\\FileZilla FTP Client\\filezilla.exe",
    "winrar": "C:\\Program Files\\WinRAR\\WinRAR.exe",
    "7zip": "C:\\Program Files\\7-Zip\\7zFM.exe",
    "obs studio": "C:\\Program Files\\obs-studio\\bin\\64bit\\obs64.exe",
    "camtasia": "C:\\Program Files\\TechSmith\\Camtasia 2023\\CamtasiaStudio.exe"
}
