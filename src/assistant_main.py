# assistant_main.py
import pyttsx3
import threading
import webbrowser
import datetime
import wikipedia
import os
from ddgs import DDGS

engine = pyttsx3.init()
engine.setProperty('rate', 170)
is_speaking = False

def speak(text):
    global is_speaking
    def _speak():
        global is_speaking
        is_speaking = True
        engine.say(text)
        engine.runAndWait()
        is_speaking = False
    threading.Thread(target=_speak).start()

def stop_speaking():
    global is_speaking
    if is_speaking:
        engine.stop()
        is_speaking = False
        print("🛑 Jarvis stopped speaking.")

def search_info(query):
    try:
        return wikipedia.summary(query, sentences=2)
    except:
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=1))
                return results[0]['body'] if results else "No result found."
        except:
            return "Internet connection error."

def perform_action(command):
    command = command.lower()

    if "open youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://youtube.com")

    elif "open whatsapp" in command:
        speak("Opening WhatsApp Web.")
        webbrowser.open("https://web.whatsapp.com/")

    elif "open file" in command:
        file = command.replace("open file", "").strip()
        if os.path.exists(file):
            speak(f"Opening {file}")
            os.startfile(file)
        else:
            speak("File not found.")

    elif "delete file" in command:
        file = command.replace("delete file", "").strip()
        if os.path.exists(file):
            os.remove(file)
            speak("File deleted successfully.")
        else:
            speak("File not found.")

    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}")

    elif "stop speaking" in command:
        stop_speaking()

    elif any(word in command for word in ["bye", "exit", "quit"]):
        speak("Goodbye, take care!")
        exit()

    else:
        result = search_info(command)
        print("Jarvis:", result)
        speak(result)

# Start the assistant
if __name__ == "__main__":
    speak("Hello, I am your smart assistant Jarvis. How can I help you today?")
    while True:
        query = input("\nYou: ").lower().strip()
        if query:
            perform_action(query)
