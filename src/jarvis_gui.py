# jarvis_gui.py
import tkinter as tk
from tkinter import scrolledtext, ttk
import pyttsx3
import threading
import queue
import wikipedia
from ddgs import DDGS
import webbrowser
import datetime
import os
import random
import subprocess
import psutil  # For closing apps

# -----------------------------
# SPEECH SETUP
# -----------------------------
engine = pyttsx3.init()
engine.setProperty('rate', 170)

speech_queue = queue.Queue()

def speak_worker():
    while True:
        text = speech_queue.get()
        if text is None:
            break
        engine.say(text)
        engine.runAndWait()
        speech_queue.task_done()

speech_thread = threading.Thread(target=speak_worker, daemon=True)
speech_thread.start()

def speak_text(text):
    speech_queue.put(text)

def stop_speaking():
    engine.stop()

# -----------------------------
# SMART SEARCH FUNCTIONS
# -----------------------------
def search_wikipedia_or_duckduckgo(query):
    try:
        result = wikipedia.summary(query, sentences=3)
        return result
    except:
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=1))
                if results:
                    return results[0]['body']
                else:
                    return "Sorry, I couldn't find information about that."
        except:
            return "Sorry, I couldn't connect to the internet."

# -----------------------------
# GUI SAFE CHAT APPEND
# -----------------------------
def append_chat(text):
    chat_box.after(0, lambda: _append(text))

def _append(text):
    chat_box.config(state="normal")
    chat_box.insert(tk.END, text + "\n\n")
    chat_box.config(state="disabled")
    chat_box.see(tk.END)

# -----------------------------
# APPLICATION MAPPING
# -----------------------------
apps_paths = {
    "vs code": r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "vscode": r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
    "notepad": "notepad.exe",
    "whatsapp": r"C:\Users\%USERNAME%\AppData\Local\WhatsApp\WhatsApp.exe",
    "calculator": "calc.exe",
    "music": os.path.expanduser("~/Music"),
    "downloads": os.path.expanduser("~/Downloads"),
    "documents": os.path.expanduser("~/Documents"),
    "desktop": os.path.expanduser("~/Desktop"),
    "photos": os.path.expanduser("~/Pictures"),
}

# -----------------------------
# EXECUTE SYSTEM COMMANDS
# -----------------------------
def execute_system_command(command):
    command = command.lower().strip()

    # -------------------- OPEN / CLOSE APPS --------------------
    if command.startswith("open "):
        item = command.replace("open ", "").strip()
        if item in apps_paths:
            path = os.path.expandvars(apps_paths[item])
            try:
                if os.path.isdir(path):
                    os.startfile(path)
                else:
                    subprocess.Popen(path)
                speak_text(f"Opening {item}")
                append_chat(f"Jarvis: Opening {item}")
            except Exception as e:
                speak_text(f"Cannot open {item}. Error: {e}")
                append_chat(f"Jarvis: Cannot open {item}. Error: {e}")
        else:
            speak_text(f"Sorry, I could not find {item}")
            append_chat(f"Jarvis: Sorry, I could not find {item}")
        return

    elif command.startswith("close "):
        item = command.replace("close ", "").strip()
        if item in apps_paths:
            app_name = os.path.basename(apps_paths[item]).replace(".exe", "")
            closed = False
            for proc in psutil.process_iter():
                if proc.name().lower() == app_name.lower() + ".exe":
                    proc.terminate()
                    closed = True
            if closed:
                speak_text(f"Closed {item}")
                append_chat(f"Jarvis: Closed {item}")
            else:
                speak_text(f"{item} is not running")
                append_chat(f"Jarvis: {item} is not running")
        else:
            speak_text(f"Sorry, I cannot close {item}")
            append_chat(f"Jarvis: Sorry, I cannot close {item}")
        return

    # -------------------- OPEN WEBSITES --------------------
    elif "open youtube" in command:
        speak_text("Opening YouTube for you.")
        append_chat("Jarvis: Opening YouTube for you.")
        webbrowser.open("https://youtube.com")
        return
    
    elif "open google" in command:
        speak_text("Opening Google for you.")
        append_chat("Jarvis: Opening Google for you.")
        webbrowser.open("https://google.com")
        return

    # -------------------- TIME --------------------
    elif "time" in command:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        speak_text(f"The time is {now}")
        append_chat(f"Jarvis: The time is {now}")
        return

    # -------------------- MOTIVATION --------------------
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

    # -------------------- WIKIPEDIA / DUCKDUCKGO --------------------
    else:
        result = search_wikipedia_or_duckduckgo(command)
        append_chat("Jarvis: " + result)
        speak_text(result)

# -----------------------------
# GUI COMMAND PROCESS
# -----------------------------
def process_command():
    query = user_input.get().strip()
    if not query:
        return
    append_chat("You: " + query)
    user_input.delete(0, tk.END)
    
    if query.lower() in ["bye", "exit", "quit"]:
        speak_text("Goodbye! Have a nice day.")
        append_chat("Jarvis: Goodbye! Have a nice day.")
        root.after(1000, root.destroy)
        return

    if query.lower() == "stop":
        stop_speaking()
        return
    
    threading.Thread(target=execute_system_command, args=(query,), daemon=True).start()

# -----------------------------
# BEAUTIFUL FRONTEND (UI)
# -----------------------------
root = tk.Tk()
root.title("💬 Jarvis - Your Smart Assistant")
root.geometry("900x650")
root.config(bg="#1e1e2f")

# HEADER
header = tk.Label(
    root,
    text="🤖 JARVIS AI ASSISTANT",
    font=("Helvetica", 22, "bold"),
    bg="#1e1e2f",
    fg="#00ffff",
)
header.pack(pady=10)

# CHAT BOX
chat_frame = tk.Frame(root, bg="#2a2a3d", bd=3, relief="groove")
chat_frame.pack(padx=20, pady=10, fill="both", expand=True)

chat_box = scrolledtext.ScrolledText(
    chat_frame,
    wrap=tk.WORD,
    font=("Consolas", 12),
    bg="#2a2a3d",
    fg="#e0e0e0",
    insertbackground="#00ffff",
    relief="flat",
)
chat_box.pack(fill="both", expand=True, padx=10, pady=10)
chat_box.config(state="disabled")

# USER ENTRY
input_frame = tk.Frame(root, bg="#1e1e2f")
input_frame.pack(pady=10, fill="x", padx=20)

user_input = ttk.Entry(
    input_frame,
    font=("Consolas", 13),
)
user_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
user_input.focus()

style = ttk.Style()
style.configure(
    "TButton",
    font=("Helvetica", 12, "bold"),
    background="#00ffff",
    foreground="#1e1e2f",
    padding=6,
)

send_button = ttk.Button(input_frame, text="Send", command=process_command)
send_button.pack(side="right")

# FOOTER
footer = tk.Label(
    root,
    text="✨ Developed by Harshada • Powered by Python AI ✨",
    font=("Helvetica", 10),
    bg="#1e1e2f",
    fg="#888888",
)
footer.pack(side="bottom", pady=5)

root.bind('<Return>', lambda event: process_command())

# START MESSAGE
append_chat("Jarvis: Hello! I am your smart assistant. Type or speak your command below.")
speak_text("Hello! I am your smart assistant. Type or speak your command below.")

# -----------------------------
# MAIN LOOP
# -----------------------------
def main():
    root.mainloop()

if __name__ == "__main__":
    main()
