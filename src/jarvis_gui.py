# jarvis_gui.py
import tkinter as tk
from tkinter import scrolledtext, ttk
import pyttsx3
import threading
import queue
import webbrowser
import datetime
import os
import subprocess
import random

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
# EXECUTE SYSTEM COMMANDS
# -----------------------------
def execute_system_command(command):
    command = command.lower().strip()
    
    # -------------------- Websites --------------------
    if "open youtube" in command:
        speak_text("Opening YouTube")
        append_chat("Jarvis: Opening YouTube")
        webbrowser.open("https://youtube.com")
        return
    elif "open google" in command:
        speak_text("Opening Google")
        append_chat("Jarvis: Opening Google")
        webbrowser.open("https://google.com")
        return
    elif "time" in command:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        speak_text(f"The time is {now}")
        append_chat(f"Jarvis: The time is {now}")
        return
    elif "motivate" in command:
        quotes = [
            "Keep pushing, you can do it!",
            "Believe in yourself!",
            "Every day is a new opportunity."
        ]
        msg = random.choice(quotes)
        speak_text(msg)
        append_chat(f"Jarvis: {msg}")
        return

    # -------------------- Open/Close Apps and Files --------------------
    apps_paths = {
        "vs code": r"C:\Users\harsh\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        "notepad": r"C:\Windows\System32\notepad.exe",
        "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
        "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "whatsapp": r"C:\Users\harsh\AppData\Local\WhatsApp\WhatsApp.exe",
        "calculator": r"C:\Windows\System32\calc.exe",
    }

    folders_paths = {
        "desktop": os.path.expanduser("~/Desktop"),
        "documents": os.path.expanduser("~/Documents"),
        "downloads": os.path.expanduser("~/Downloads"),
        "music": os.path.expanduser("~/Music"),
        "pictures": os.path.expanduser("~/Pictures"),
        "videos": os.path.expanduser("~/Videos"),
    }

    # Open apps
    for name, path in apps_paths.items():
        if name in command:
            try:
                if "close" in command:
                    os.system(f"taskkill /f /im {os.path.basename(path)}")
                    speak_text(f"Closing {name}")
                    append_chat(f"Jarvis: Closing {name}")
                else:
                    subprocess.Popen(path)
                    speak_text(f"Opening {name}")
                    append_chat(f"Jarvis: Opening {name}")
            except Exception as e:
                speak_text(f"Cannot open {name}. Error: {str(e)}")
                append_chat(f"Jarvis: Cannot open {name}. Error: {str(e)}")
            return

    # Open folders
    for name, path in folders_paths.items():
        if name in command:
            try:
                os.startfile(path)
                speak_text(f"Opening {name}")
                append_chat(f"Jarvis: Opening {name}")
            except Exception as e:
                speak_text(f"Cannot open {name}. Error: {str(e)}")
                append_chat(f"Jarvis: Cannot open {name}. Error: {str(e)}")
            return

    speak_text("Sorry, I did not understand the command.")
    append_chat("Jarvis: Sorry, I did not understand the command.")

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
        speak_text("Goodbye!")
        append_chat("Jarvis: Goodbye!")
        root.after(1000, root.destroy)
        return
    if query.lower() == "stop":
        stop_speaking()
        return

    threading.Thread(target=execute_system_command, args=(query,), daemon=True).start()

# -----------------------------
# GUI LAYOUT
# -----------------------------
root = tk.Tk()
root.title("💬 Jarvis AI Assistant")
root.geometry("900x650")
root.config(bg="#1e1e2f")

# Header
header = tk.Label(root, text="🤖 JARVIS AI ASSISTANT", font=("Helvetica", 22, "bold"),
                  bg="#1e1e2f", fg="#00ffff")
header.pack(pady=10)

# Chat box
chat_frame = tk.Frame(root, bg="#2a2a3d", bd=3, relief="groove")
chat_frame.pack(padx=20, pady=10, fill="both", expand=True)

chat_box = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, font=("Consolas", 12),
                                     bg="#2a2a3d", fg="#e0e0e0", insertbackground="#00ffff", relief="flat")
chat_box.pack(fill="both", expand=True, padx=10, pady=10)
chat_box.config(state="disabled")

# User input
input_frame = tk.Frame(root, bg="#1e1e2f")
input_frame.pack(pady=10, fill="x", padx=20)

user_input = ttk.Entry(input_frame, font=("Consolas", 13))
user_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
user_input.focus()

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12, "bold"), background="#00ffff", foreground="#1e1e2f", padding=6)

send_button = ttk.Button(input_frame, text="Send", command=process_command)
send_button.pack(side="right")

# Footer
footer = tk.Label(root, text="✨ Developed by Harshada • Powered by Python AI ✨",
                  font=("Helvetica", 10), bg="#1e1e2f", fg="#888888")
footer.pack(side="bottom", pady=5)

root.bind('<Return>', lambda event: process_command())

# Start message
append_chat("Jarvis: Hello! I am your smart assistant. Type your command below.")
speak_text("Hello! I am your smart assistant. Type your command below.")

# -----------------------------
# MAIN FUNCTION
# -----------------------------
def main():
    root.mainloop()

if __name__ == "__main__":
    main()
