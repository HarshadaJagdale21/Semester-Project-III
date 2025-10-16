import os
import tkinter as tk
import pyttsx3
import speech_recognition as sr
import subprocess
import webbrowser
import psutil
import wikipedia
import dataset
import time
import threading
import queue

# ===================== VOICE ENGINE ==========================
engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)

# --- Speech queue + worker to avoid run loop conflicts ---
_speech_queue = queue.Queue()

def _speech_worker():
    while True:
        text = _speech_queue.get()
        if text is None:
            break
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("Speech error:", e)
        _speech_queue.task_done()

_speech_thread = threading.Thread(target=_speech_worker, daemon=True)
_speech_thread.start()

def speak(text):
    """Queue text to be spoken by background speech thread."""
    print(f"Jarvis: {text}")
    try:
        _speech_queue.put(text)
    except Exception as e:
        print("Failed to queue speech:", e)

# ===================== HELPER: THREAD-SAFE GUI UPDATES ========
def update_status(text, fg="white"):
    """Set status_label text in the main GUI thread."""
    try:
        # status_label is created in main(); use after to call on main thread
        status_label.after(0, lambda: status_label.config(text=text, fg=fg))
    except Exception:
        # if status_label not yet defined, safe fallback to print
        print("STATUS:", text)

# ===================== SEARCH FILE FUNCTION =================
def find_file(filename, search_paths=["C:\\", "D:\\", "E:\\"]):
    """Search entire drives for an app or file by name (returns first matching .exe or file)."""
    filename_lower = filename.lower()
    for path in search_paths:
        # skip missing drives to avoid long exceptions
        if not os.path.exists(path):
            continue
        for root, dirs, files in os.walk(path):
            for file in files:
                if filename_lower in file.lower():
                    return os.path.join(root, file)
    return None

# ===================== OPEN FILE/APP ========================
def open_item(item_name):
    speak(f"Searching for {item_name}")
    path = dataset.DATASET.get(item_name.lower())

    # 1) Try dataset path
    if path:
        try:
            # If URL, open in browser
            if isinstance(path, str) and (path.startswith("http://") or path.startswith("https://")):
                webbrowser.open(path)
                speak(f"Opening {item_name} in your browser.")
                return
            # Expand environment variables like %USERNAME% or %USERPROFILE%
            expanded = os.path.expandvars(path)
            # If folder path, open explorer
            if os.path.isdir(expanded):
                os.startfile(expanded)
                speak(f"Opening folder {item_name}")
                return
            # Try startfile / subprocess
            try:
                os.startfile(expanded)
            except Exception:
                subprocess.Popen(expanded)
            speak(f"Opening {item_name}")
            return
        except Exception as e:
            speak(f"Cannot open {item_name}. Error: {e}")

    # 2) Try to locate on disk if not in dataset
    speak("Looking for the item on your computer. This may take a moment.")
    update_status(f"Searching for {item_name}...", "yellow")
    found = find_file(item_name)
    if found:
        try:
            # If file is an executable or other file, open it
            os.startfile(found)
            speak(f"Found and opened {item_name}")
            # cache it in dataset for faster next time (in-memory only)
            try:
                dataset.DATASET[item_name.lower()] = found
            except Exception:
                pass
        except Exception as e:
            speak(f"Could not open {item_name}. Error: {e}")
    else:
        speak(f"Sorry, I couldn't find {item_name} on your PC.")
    update_status("Ready", "white")

# ===================== CLOSE APP ============================
def close_item(app_name):
    speak(f"Trying to close {app_name}")
    closed_any = False
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            pname = proc.info['name'] or ""
            if app_name.lower() in pname.lower():
                proc.kill()
                closed_any = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    if closed_any:
        speak(f"Closed {app_name}")
    else:
        speak(f"No running app named {app_name} found.")

# ===================== CLOSE ALL APPS =======================
def close_all_apps():
    speak("Closing all open applications except system processes.")
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            name = proc.info['name'] or ""
            # skip explorer and python to avoid locking you out
            if name.lower() not in ["explorer.exe", "python.exe", "pythonw.exe"]:
                proc.kill()
        except Exception:
            pass
    speak("All applications have been closed.")

# ===================== WIKIPEDIA INFO =======================
def get_information(query):
    try:
        update_status("Searching Wikipedia...", "yellow")
        speak(f"Searching for {query} on Wikipedia.")
        result = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia, " + result)
    except wikipedia.DisambiguationError:
        speak(f"Too many results for {query}. Try being more specific.")
    except wikipedia.PageError:
        speak(f"Sorry, I couldn't find any information about {query}.")
    except Exception:
        speak("Something went wrong while searching.")
    update_status("Ready", "white")

# ===================== SYSTEM COMMANDS ======================
def shutdown_pc():
    speak("Shutting down the computer in 5 seconds.")
    time.sleep(5)
    os.system("shutdown /s /t 1")

def restart_pc():
    speak("Restarting the computer in 5 seconds.")
    time.sleep(5)
    os.system("shutdown /r /t 1")

def lock_pc():
    speak("Locking the computer now.")
    os.system("rundll32.exe user32.dll,LockWorkStation")

# ===================== LISTEN (runs in a background thread) =
def _listen_and_handle():
    """Blocking function to listen and then handle command. Runs in background thread."""
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            update_status("🎧 Listening...", "yellow")
            speak("I am listening. Please say your command.")
            # blocking call that can take a few seconds
            audio = recognizer.listen(source, phrase_time_limit=6)
    except Exception as e:
        update_status("Microphone error", "red")
        speak("Microphone error. Please check your microphone.")
        print("Microphone error:", e)
        return

    try:
        update_status("Processing...", "lightgreen")
        command = recognizer.recognize_google(audio).lower()
        update_status(f"🎤 You said: {command}", "cyan")
        speak(f"You said {command}")
    except sr.UnknownValueError:
        update_status("❌ Didn't catch that.", "red")
        speak("Sorry, I didn't catch that. Please try again.")
        return
    except sr.RequestError:
        update_status("⚠️ Speech recognition error", "red")
        speak("Speech recognition service is not available. Try typing your command.")
        return

    # call the handler (this may itself do disk IO etc; it runs in background thread)
    try:
        handle_command(command)
    except Exception as e:
        print("Error handling command:", e)
    finally:
        update_status("Ready", "white")

def listen_command():
    """Non-blocking wrapper called by GUI button; starts background thread."""
    t = threading.Thread(target=_listen_and_handle, daemon=True)
    t.start()

# ===================== HANDLE COMMANDS =====================
def handle_command(command):
    if not command:
        speak("I did not hear anything. Please repeat.")
        return

    update_status(f"Processing command: {command}", "white")
    speak("Processing your command.")

    cmd = command.lower().strip()

    if cmd.startswith("open "):
        item = cmd.replace("open ", "", 1).strip()
        # run open in background thread (avoid blocking even further)
        th = threading.Thread(target=open_item, args=(item,), daemon=True)
        th.start()
        return

    if cmd.startswith("close all"):
        th = threading.Thread(target=close_all_apps, daemon=True)
        th.start()
        return

    if cmd.startswith("close "):
        app = cmd.replace("close ", "", 1).strip()
        th = threading.Thread(target=close_item, args=(app,), daemon=True)
        th.start()
        return

    if cmd.startswith("search "):
        query = cmd.replace("search ", "", 1).strip()
        speak(f"Searching for {query} on Google.")
        update_status(f"🌐 Searching for {query}...", "yellow")
        webbrowser.open(f"https://www.google.com/search?q={query}")
        update_status("Ready", "white")
        return

    if any(word in cmd for word in ["what", "who", "when", "where", "tell me"]):
        query = cmd.replace("jarvis", "").replace("tell me", "").strip()
        # run wiki search in background
        th = threading.Thread(target=get_information, args=(query,), daemon=True)
        th.start()
        return

    if "shutdown" in cmd or "turn off" in cmd:
        th = threading.Thread(target=shutdown_pc, daemon=True)
        th.start()
        return

    if "restart" in cmd:
        th = threading.Thread(target=restart_pc, daemon=True)
        th.start()
        return

    if "lock" in cmd:
        th = threading.Thread(target=lock_pc, daemon=True)
        th.start()
        return

    if cmd in ["exit", "quit"]:
        speak("Goodbye Harshada! Have a great day.")
        # stop speech worker gracefully
        try:
            _speech_queue.put(None)
        except Exception:
            pass
        root.after(200, root.destroy)
        return

    speak("Sorry, I didn't understand that command.")
    update_status("⚠️ Unknown command", "red")

# ===================== MAIN UI ============================
def main():
    global root, status_label
    root = tk.Tk()
    root.title("Jarvis Voice Assistant - Smart Mode")
    root.geometry("600x550")
    root.configure(bg="#101820")

    tk.Label(root, text="🤖 JARVIS - Smart Voice Assistant",
             font=("Arial", 18, "bold"), fg="white", bg="#101820").pack(pady=15)

    command_entry = tk.Entry(root, font=("Arial", 14))
    command_entry.pack(pady=10, ipadx=10, ipady=5, fill=tk.X, padx=20)

    def run_command():
        command = command_entry.get().lower()
        if command:
            # speak feedback for typed commands
            speak(f"You typed: {command}")
            # handle in background
            th = threading.Thread(target=handle_command, args=(command,), daemon=True)
            th.start()
        command_entry.delete(0, tk.END)

    tk.Button(root, text="Run Command", font=("Arial", 12), command=run_command).pack(pady=10)
    # Changed 🎤 Speak button to call non-blocking listen_command() wrapper
    tk.Button(root, text="🎤 Speak", font=("Arial", 12), command=listen_command).pack(pady=10)
    tk.Button(root, text="Exit", font=("Arial", 12), command=lambda: root.destroy()).pack(pady=10)

    status_label = tk.Label(root, text="Status: Ready", font=("Arial", 12),
                            fg="white", bg="#101820")
    status_label.pack(pady=20)

    speak("Hello Harshada! I am your Jarvis. All systems are online and voice activated. How can I assist you now?")
    root.mainloop()

if __name__ == "__main__":
    main()
