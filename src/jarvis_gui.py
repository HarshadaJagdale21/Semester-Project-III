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
import speech_recognition as sr

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
# EXECUTE USER COMMANDS
# -----------------------------
def execute_system_command(command):
    command = command.lower().strip()
    
    # -------------------- Open websites --------------------
    if "open youtube" in command:
        speak_text("Opening YouTube for you.")
        append_chat("Jarvis: Opening YouTube for you.")
        webbrowser.open("https://youtube.com")
        return
    elif "open google" in command:
        speak_text("Opening Google for you.")
        append_chat("Jarvis: Opening Google for you.")
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
            "Believe in yourself and all that you are.",
            "Every day is a new opportunity to shine."
        ]
        message = random.choice(quotes)
        speak_text(message)
        append_chat(f"Jarvis: {message}")
        return

    # -------------------- Open files / apps --------------------
    elif "open " in command or "close " in command:
        action = "open" if "open " in command else "close"
        item_name = command.replace(action + " ", "").strip().lower()
        found = False

        # Predefined app/folder paths (expand as needed)
        apps_dataset = {
            "vs code": r"C:\Users\harsh\AppData\Local\Programs\Microsoft VS Code\Code.exe",
            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
            "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
            "notepad": r"C:\Windows\System32\notepad.exe",
            "whatsapp": r"C:\Users\harsh\AppData\Local\WhatsApp\WhatsApp.exe",
            "downloads": os.path.expanduser("~/Downloads"),
            "documents": os.path.expanduser("~/Documents"),
            "desktop": os.path.expanduser("~/Desktop"),
            "pictures": os.path.expanduser("~/Pictures"),
            "music": os.path.expanduser("~/Music"),
            "videos": os.path.expanduser("~/Videos")
        }

        if item_name in apps_dataset:
            path = apps_dataset[item_name]
            try:
                if action == "open":
                    speak_text(f"Opening {item_name}")
                    append_chat(f"Jarvis: Opening {item_name}")
                    os.startfile(path)
                else:
                    speak_text(f"Closing {item_name}")
                    append_chat(f"Jarvis: Closing {item_name}")
                    os.system(f"taskkill /f /im {os.path.basename(path)}")
                found = True
            except Exception as e:
                speak_text(f"Cannot {action} {item_name}. Error: {e}")
                append_chat(f"Jarvis: Cannot {action} {item_name}. Error: {e}")
        if not found:
            speak_text(f"Cannot find {item_name} to {action}.")
            append_chat(f"Jarvis: Cannot find {item_name} to {action}.")
        return

    # -------------------- Wikipedia / DuckDuckGo --------------------
    else:
        result = search_wikipedia_or_duckduckgo(command)
        append_chat("Jarvis: " + result)
        speak_text(result)

# -----------------------------
# VOICE COMMAND
# -----------------------------
def listen_voice_command():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    append_chat("🎤 Listening for voice command...")
    speak_text("Listening for your command")
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
        command = recognizer.recognize_google(audio)
        append_chat(f"You (voice): {command}")
        threading.Thread(target=execute_system_command, args=(command,), daemon=True).start()
    except sr.UnknownValueError:
        append_chat("Jarvis: Sorry, I did not understand that.")
        speak_text("Sorry, I did not understand that")
    except sr.RequestError:
        append_chat("Jarvis: Sorry, the speech service is unavailable.")
        speak_text("Sorry, the speech service is unavailable")
    except Exception as e:
        append_chat(f"Jarvis: Error: {e}")
        speak_text(f"Error: {e}")

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

voice_button = ttk.Button(input_frame, text="🎤 Speak", command=listen_voice_command)
voice_button.pack(side="right", padx=(5,0))

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
root.bind('<F2>', lambda event: listen_voice_command())

# START MESSAGE
append_chat("Jarvis: Hello , I am your smart assistant. Type or speak your command below.")
speak_text("Hello , I am your smart assistant. Type or speak your command below.")

# -----------------------------
# MAIN LOOP
# -----------------------------
def main():
    root.mainloop()

if __name__ == "__main__":
    main()
