# jarvis_gui.py
import tkinter as tk
from tkinter import scrolledtext, ttk
import pyttsx3
import threading
import queue
import os
import webbrowser
import datetime
import speech_recognition as sr
from dataset import DATASET

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
# GUI CHAT BOX APPEND
# -----------------------------
def append_chat(text):
    chat_box.after(0, lambda: _append(text))

def _append(text):
    chat_box.config(state="normal")
    chat_box.insert(tk.END, text + "\n\n")
    chat_box.config(state="disabled")
    chat_box.see(tk.END)

# -----------------------------
# OPEN / CLOSE COMMANDS
# -----------------------------
open_processes = {}  # Track opened apps to close

def execute_system_command(command):
    command = command.lower().strip()

    # -------------------- OPEN / CLOSE APPS --------------------
    if command.startswith("open "):
        name = command.replace("open ", "").strip()
        name_key = name.lower()
        if name_key in DATASET:
            path = DATASET[name_key].replace("%USERNAME%", os.getlogin())
            try:
                proc = os.startfile(path)
                open_processes[name_key] = path
                speak_text(f"Opening {name}")
                append_chat(f"Jarvis: Opening {name}")
            except Exception as e:
                speak_text(f"Cannot open {name}. Error: {e}")
                append_chat(f"Jarvis: Cannot open {name}. Error: {e}")
        else:
            speak_text(f"Sorry, I could not find {name}")
            append_chat(f"Jarvis: Sorry, I could not find {name}")
        return

    elif command.startswith("close "):
        name = command.replace("close ", "").strip()
        name_key = name.lower()
        if name_key in open_processes:
            try:
                os.system(f"taskkill /f /im {os.path.basename(open_processes[name_key])}")
                speak_text(f"Closed {name}")
                append_chat(f"Jarvis: Closed {name}")
                del open_processes[name_key]
            except Exception as e:
                speak_text(f"Cannot close {name}. Error: {e}")
                append_chat(f"Jarvis: Cannot close {name}. Error: {e}")
        else:
            speak_text(f"{name} is not currently opened")
            append_chat(f"Jarvis: {name} is not currently opened")
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
        message = quotes[datetime.datetime.now().second % len(quotes)]
        speak_text(message)
        append_chat(f"Jarvis: {message}")
        return

    # -------------------- FALLBACK --------------------
    else:
        speak_text("Sorry, I didn’t understand that.")
        append_chat("Jarvis: Sorry, I didn’t understand that.")

# -----------------------------
# VOICE COMMANDS
# -----------------------------
def listen_voice():
    r = sr.Recognizer()
    mic = sr.Microphone()
    append_chat("🎤 Listening...")
    speak_text("Listening...")
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=5)
        command = r.recognize_google(audio)
        append_chat(f"You (voice): {command}")
        threading.Thread(target=execute_system_command, args=(command,), daemon=True).start()
    except sr.WaitTimeoutError:
        append_chat("🎤 Listening timed out. Say your command again.")
    except Exception as e:
        append_chat(f"🎤 Voice error: {e}")

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
# BEAUTIFUL FRONTEND (UI ONLY)
# -----------------------------
root = tk.Tk()
root.title("💬 Jarvis - Your Smart Assistant")
root.geometry("900x650")
root.config(bg="#1e1e2f")

header = tk.Label(root, text="🤖 JARVIS AI ASSISTANT", font=("Helvetica", 22, "bold"), bg="#1e1e2f", fg="#00ffff")
header.pack(pady=10)

chat_frame = tk.Frame(root, bg="#2a2a3d", bd=3, relief="groove")
chat_frame.pack(padx=20, pady=10, fill="both", expand=True)

chat_box = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, font=("Consolas", 12), bg="#2a2a3d", fg="#e0e0e0", insertbackground="#00ffff", relief="flat")
chat_box.pack(fill="both", expand=True, padx=10, pady=10)
chat_box.config(state="disabled")

input_frame = tk.Frame(root, bg="#1e1e2f")
input_frame.pack(pady=10, fill="x", padx=20)

user_input = ttk.Entry(input_frame, font=("Consolas", 13))
user_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
user_input.focus()

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12, "bold"), background="#00ffff", foreground="#1e1e2f", padding=6)

send_button = ttk.Button(input_frame, text="Send", command=process_command)
send_button.pack(side="right")

voice_button = ttk.Button(input_frame, text="🎤 Speak", command=listen_voice)
voice_button.pack(side="right", padx=10)

footer = tk.Label(root, text="✨ Developed by Harshada • Powered by Python AI ✨", font=("Helvetica", 10), bg="#1e1e2f", fg="#888888")
footer.pack(side="bottom", pady=5)

root.bind('<Return>', lambda event: process_command())

append_chat("Jarvis: Hello! I am your smart assistant. Type or speak your command below.")
speak_text("Hello! I am your smart assistant. Type or speak your command below.")

# -----------------------------
# MAIN LOOP
# -----------------------------
def main():
    root.mainloop()

if __name__ == "__main__":
    main()
