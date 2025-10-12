import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)
engine.say("Hello Harshada. This is a voice test.")
engine.runAndWait()
