# dataset.py
import os

# Expand user folders
USER = os.path.expanduser("~")

dataset = {
    # Browsers
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    
    # Microsoft Office
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
    "onenote": r"C:\Program Files\Microsoft Office\root\Office16\ONENOTE.EXE",
    
    # System apps
    "notepad": r"C:\Windows\System32\notepad.exe",
    "calculator": r"C:\Windows\System32\calc.exe",
    "paint": r"C:\Windows\System32\mspaint.exe",
    "cmd": r"C:\Windows\System32\cmd.exe",
    "explorer": r"C:\Windows\explorer.exe",
    "task manager": r"C:\Windows\System32\Taskmgr.exe",
    
    # Common folders
    "desktop": os.path.join(USER, "Desktop"),
    "documents": os.path.join(USER, "Documents"),
    "downloads": os.path.join(USER, "Downloads"),
    "music": os.path.join(USER, "Music"),
    "pictures": os.path.join(USER, "Pictures"),
    "videos": os.path.join(USER, "Videos"),
    
    # Messaging apps (if installed)
    "whatsapp": r"C:\Users\{0}\AppData\Local\WhatsApp\WhatsApp.exe".format(USER.split("\\")[-1]),
    "telegram": r"C:\Users\{0}\AppData\Roaming\Telegram Desktop\Telegram.exe".format(USER.split("\\")[-1]),
    
    # IDEs / Editors
    "vscode": r"C:\Users\{0}\AppData\Local\Programs\Microsoft VS Code\Code.exe".format(USER.split("\\")[-1]),
    "pycharm": r"C:\Program Files\JetBrains\PyCharm Community Edition 2023.1.2\bin\pycharm64.exe",
    
    # Media players
    "vlc": r"C:\Program Files\VideoLAN\VLC\vlc.exe",
    
    # Browsing local files
    "downloads folder": os.path.join(USER, "Downloads"),
    "documents folder": os.path.join(USER, "Documents"),
    
    # Add more apps or folders here...
}
