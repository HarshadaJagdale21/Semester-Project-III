import os
import tkinter as tk
import pyttsx3
import speech_recognition as sr
import subprocess
import webbrowser
import psutil
import dataset  # your app/folder dataset

# ========== VOICE ENGINE ==========
engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

# ========== FILE SEARCH ==========
def find_file(filename, search_paths=["C:\\", "D:\\", "E:\\"]):
    for path in search_paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                if filename.lower() in file.lower():
                    return os.path.join(root, file)
    return None

# ========== OPEN ITEM ==========
def open_item(item_name):
    path = dataset.DATASET.get(item_name.lower())

    if path:
        try:
            os.startfile(os.path.expandvars(path))
            speak(f"Opening {item_name}")
            return
        except Exception as e:
            speak(f"Cannot open {item_name}. Error: {e}")
            return

    # Search in file system
    speak(f"Searching for {item_name}...")
    found = find_file(item_name)
    if found:
        try:
            os.startfile(found)
            speak(f"Found and opened {item_name}")
        except Exception as e:
            speak(f"Could not open {item_name}")
            print(e)
    else:
        speak(f"Sorry, I could not find {item_name}")

# ========== CLOSE ITEM ==========
def close_item(app_name):
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
        speak(f"Couldn't find any app named {app_name} running")

# ========== CLOSE ALL ==========
def close_all_apps():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'].lower() not in ["explorer.exe", "python.exe"]:
                proc.kill()
        except Exception:
            pass
    speak("All applications have been closed.")

# ========== VOICE INPUT ==========
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        audio = recognizer.listen(source, phrase_time_limit=5)
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Speech recognition service is down.")
        return ""

# ========== HANDLE COMMAND ==========
def handle_command(command):
    if not command:
        return

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
        webbrowser.open(f"https://www.google.com/search?q={query}")
    elif "exit" in command or "quit" in command:
        speak("Goodbye Harshada! See you soon.")
        root.destroy()
    else:
        speak("Sorry, I didn’t understand that command.")

# ========== GUI SETUP ==========
def main():
    global root
    root = tk.Tk()
    root.title("Jarvis Voice Assistant")
    root.geometry("520x500")
    root.configure(bg="#121212")

    tk.Label(root, text="🎙️ JARVIS - Your Smart Voice Assistant",
             font=("Arial", 16, "bold"), fg="white", bg="#121212").pack(pady=15)

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

    speak("Hello Harshada! I am Jarvis, your smart assistant. How can I help you today?")

    root.mainloop()

if __name__ == "__main__":
    main()
