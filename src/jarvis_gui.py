# Add at the top after imports
import mysql.connector
import subprocess

# -----------------------------
# LOAD APPS DATA FROM DATABASE
# -----------------------------
def load_apps_from_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # your MySQL password
        database="jarvis_users"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT name, type, path FROM pc_apps")
    apps_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return apps_list

apps_data = load_apps_from_db()

# -----------------------------
# EXECUTE USER COMMAND (UPDATE)
# -----------------------------
def execute_system_command(command):
    command = command.lower().strip()

    # Open/Close apps or folders dynamically
    if command.startswith("open ") or command.startswith("close "):
        action = "open" if command.startswith("open ") else "close"
        item_name = command.replace(action, "").strip().lower()

        found = False
        for name, type_, path in apps_data:
            if item_name == name.lower():
                found = True
                try:
                    if action == "open":
                        if path:
                            subprocess.Popen(path)
                        else:
                            # Try opening using Windows 'start' command
                            subprocess.Popen(f'start "" "{name}"', shell=True)
                        speak_text(f"Opening {name}")
                        append_chat(f"Jarvis: Opening {name}")
                    else:
                        # Close application by name
                        subprocess.Popen(f'taskkill /im "{name}.exe" /f', shell=True)
                        speak_text(f"Closing {name}")
                        append_chat(f"Jarvis: Closing {name}")
                except Exception as e:
                    speak_text(f"Cannot {action} {name}. Error: {e}")
                    append_chat(f"Jarvis: Cannot {action} {name}. Error: {e}")
                break

        if not found:
            speak_text(f"Sorry, I could not find {item_name}")
            append_chat(f"Jarvis: Sorry, I could not find {item_name}")
        return

    # Existing website commands
    elif "youtube" in command:
        speak_text("Opening YouTube")
        append_chat("Jarvis: Opening YouTube")
        webbrowser.open("https://youtube.com")
        return
    elif "google" in command:
        speak_text("Opening Google")
        append_chat("Jarvis: Opening Google")
        webbrowser.open("https://google.com")
        return

    # Time, Motivation, Wikipedia
    elif "time" in command:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        speak_text(f"The time is {now}")
        append_chat(f"Jarvis: The time is {now}")
        return
    elif "motivate" in command:
        quotes = [
            "Keep pushing, you can do it!",
            "Believe in yourself and all that you are.",
            "Every day is a new opportunity to shine."
        ]
        message = random.choice(quotes)
        speak_text(message)
        append_chat(f"Jarvis: {message}")
        return

    # Fallback to Wikipedia / DuckDuckGo
    else:
        result = search_wikipedia_or_duckduckgo(command)
        append_chat("Jarvis: " + result)
        speak_text(result)
