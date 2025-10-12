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

# ===================== VOICE ENGINE ==========================
engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)

# ===================== SPEAK FUNCTION ==========================
def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

# ===================== SEARCH FILE FUNCTION =====================
def find_file(filename, search_paths=["C:\\", "D:\\", "E:\\"]):
    for path in search_paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                if filename.lower() in file.lower():
                    return os.path.join(root, file)
    return None

# ===================== OPEN FILE/APP =====================
def open_item(item_name):
    speak(f"Searching for {item_name}")
    path = dataset.DATASET.get(item_name.lower())
    if path:
        try:
            os.startfile(os.path.expandvars(path))
            speak(f"Opening {item_name}")
            return
        except Exception as e:
            speak(f"Cannot open {item_name}. Error: {e}")
            return
    speak("Looking for the file on your computer...")
    found = find_file(item_name)
    if found:
        try:
            os.startfile(found)
            speak(f"Found and opened {item_name}")
        except Exception as e:
            speak(f"Could not open {item_name}")
    else:
        speak(f"Sorry, I couldn’t find {item_name}")

# ===================== CLOSE APP =====================
def close_item(app_name):
    speak(f"Searching for any running process of {app_name}")
    closed_any = False
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if app_name.lower() in proc.info['name'].lower():
                proc.kill()
                closed_any = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    if closed_any:
        speak(f"Closed {app_name}")
    else:
        speak(f"No running app named {app_name} found")

# ===================== CLOSE ALL APPS =====================
def close_all_apps():
    speak("Closing all open applications except system processes.")
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'].lower() not in ["explorer.exe", "python.exe"]:
                proc.kill()
        except Exception:
            pass
    speak("All applications have been closed.")

# ===================== WIKIPEDIA INFO =====================
def get_information(query):
    try:
        speak(f"Searching for {query} on Wikipedia.")
        result = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia, " + result)
    except wikipedia.DisambiguationError:
        speak(f"Too many results for {query}. Try being more specific.")
    except wikipedia.PageError:
        speak(f"Sorry, I couldn't find any information about {query}.")
    except Exception:
        speak("Something went wrong while searching.")

# ===================== SYSTEM COMMANDS =====================
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

# ===================== LISTEN TO VOICE =====================
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="🎧 Listening...", fg="yellow")
        root.update()
        speak("Listening...")
        audio = recognizer.listen(source, phrase_time_limit=5)
    try:
        command = recognizer.recognize_google(audio).lower()
        status_label.config(text=f"🎤 You said: {command}", fg="cyan")
        print(f"You said: {command}")
        speak(f"You said {command}")
        return command
    except sr.UnknownValueError:
        status_label.config(text="❌ Didn't catch that.", fg="red")
        speak("Sorry, I didn’t catch that. Please say again.")
        return ""
    except sr.RequestError:
        status_label.config(text="⚠️ Speech recognition error", fg="red")
        speak("Speech recognition service is not working right now.")
        return ""


# ===================== HANDLE COMMANDS =====================
def handle_command(command):
    if not command:
        speak(f"Processing your command {command}")

        return

    status_label.config(text=f"Processing command: {command}", fg="white")
    root.update()
    speak("Processing your command.")

    if "open" in command:
        item = command.replace("open", "").strip()
        open_item(item)

    elif "close all" in command:
        close_all_apps()

    elif "close" in command:
        app = command.replace("close", "").strip()
        close_item(app)

    elif "search" in command:
        query = command.replace("search", "").strip()
        speak(f"Searching for {query} on Google")
        status_label.config(text=f"🌐 Searching for {query}...", fg="yellow")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif any(word in command for word in ["what", "who", "when", "where", "tell me"]):
        query = command.replace("jarvis", "").replace("tell me", "").strip()
        get_information(query)

    elif "shutdown" in command or "turn off" in command:
        shutdown_pc()

    elif "restart" in command:
        restart_pc()

    elif "lock" in command:
        lock_pc()

    elif "exit" in command or "quit" in command:
        speak("Goodbye Harshada! Have a great day.")
        root.destroy()

    else:
        speak("Sorry, I didn’t understand that command.")
        status_label.config(text="⚠️ Unknown command", fg="red")

# ===================== MAIN UI =====================
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
        handle_command(command)
        command_entry.delete(0, tk.END)

    tk.Button(root, text="Run Command", font=("Arial", 12), command=run_command).pack(pady=10)
    tk.Button(root, text="🎤 Speak", font=("Arial", 12),
              command=lambda: handle_command(listen_command())).pack(pady=10)
    tk.Button(root, text="Exit", font=("Arial", 12), command=lambda: root.destroy()).pack(pady=10)

    status_label = tk.Label(root, text="Status: Ready", font=("Arial", 12),
                            fg="white", bg="#101820")
    status_label.pack(pady=20)

    speak("Hello Harshada! I am your Jarvis. All systems are online and voice activated. How can I assist you now?")
    root.mainloop()

if __name__ == "__main__":
    main()
