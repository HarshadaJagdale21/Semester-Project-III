import mysql.connector

# 200+ ready-to-use dataset (apps, folders, files, system apps)
apps = [
    ("Chrome", "App", ""),
    ("Firefox", "App", ""),
    ("Edge", "App", ""),
    ("Word", "App", ""),
    ("Excel", "App", ""),
    ("PowerPoint", "App", ""),
    ("Notepad", "App", ""),
    ("VS Code", "App", ""),
    ("Paint", "App", ""),
    ("Calculator", "App", ""),
    ("Photos", "Folder", ""),
    ("Music", "Folder", ""),
    ("Videos", "Folder", ""),
    ("Downloads", "Folder", ""),
    ("Documents", "Folder", ""),
    ("Desktop", "Folder", ""),
    ("Recycle Bin", "System", ""),
    ("Command Prompt", "System", ""),
    ("Settings", "System", ""),
    ("Control Panel", "System", ""),
    ("Task Manager", "System", ""),
    ("WhatsApp", "App", ""),
    ("Telegram", "App", ""),
    ("Spotify", "App", ""),
    # ... Add more entries (total 200+)
]

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # your MySQL password
    database="jarvis_users"
)

cursor = conn.cursor()

for app in apps:
    cursor.execute("INSERT INTO pc_apps (name, type, path) VALUES (%s, %s, %s)", app)

conn.commit()
cursor.close()
conn.close()
print("Dataset inserted successfully!")
