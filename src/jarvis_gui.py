import os
import tkinter as tk
import pyttsx3
import speech_recognition as sr
import subprocess
import dataset
import webbrowser

# ========== VOICE ENGINE ==========
engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ========== FILE SEARCH FUNCTION ==========
def find_file(filename, search_path="C:\\"):
    """Search entire system for a filename"""
    for root, dirs, files in os.walk(search_path):
        for file in files:
            if filename.lower() in file.lower():
                return os.path.join(root, file)
    return None

# ========== OPEN ITEM ==========
def open_item(item_name):
    # Check in dataset
    path = dataset.DATASET.get(item_name.lower())

    if path:
        try:
            os.startfile(os.path.expandvars(path))
            speak(f"Opening {item_name}")
            return
        except Exception as e:
            speak("Sorry, I could not open it.")
            print(e)
            return

    # Search the file system
    speak(f"Searching for {item_name}, please wait...")
    file_path = find_file(item_name)

    if file_path:
        try:
            os.startfile(file_path)
            speak(f"Found and opened {item_name}")
        except Exception as e:
            speak("Sorry, I could not open that file.")
            print(e)
    else:
        speak(f"Sorry, I could not find {item_name} on your computer.")

# ========== VOICE COMMAND ==========
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        audio = recognizer.listen(source, phrase_time_limit=5)
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"User said: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that.")
        return ""
    except sr.RequestError:
        speak("Speech service error.")
        return ""

# ========== HANDLE COMMANDS ==========
def handle_command(command):
    if not command:
        return

    if "open" in command:
        item = command.replace("open", "").strip()
        open_item(item)
    elif "close" in command:
        app = command.replace("close", "").strip()
        os.system(f"taskkill /f /im {app}.exe")
        speak(f"Closed {app}")
    elif "search" in command:
        query = command.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Searching {query} on Google")
    elif "exit" in command or "quit" in command:
        speak("Goodbye Harshada!")
        root.destroy()
    else:
        speak("Sorry, I didn’t understand that command.")

# ========== GUI SETUP ==========
def main():
    global root
    root = tk.Tk()
    root.title("Jarvis Voice Assistant")
    root.geometry("500x500")
    root.configure(bg="#121212")

    tk.Label(root, text="🎤 JARVIS - Voice Assistant", font=("Arial", 16, "bold"), fg="white", bg="#121212").pack(pady=15)

    command_entry = tk.Entry(root, font=("Arial", 14))
    command_entry.pack(pady=10, ipadx=10, ipady=5, fill=tk.X, padx=20)

    def run_command():
        command = command_entry.get().lower()
        handle_command(command)
        command_entry.delete(0, tk.END)

    tk.Button(root, text="Run Command", font=("Arial", 12), command=run_command).pack(pady=10)
    tk.Button(root, text="🎙 Speak", font=("Arial", 12), command=lambda: handle_command(listen_command())).pack(pady=10)

    tk.Button(root, text="Exit", font=("Arial", 12), command=lambda: root.destroy()).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
