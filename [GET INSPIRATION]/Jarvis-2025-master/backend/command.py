import time
import pyttsx3
import speech_recognition as sr
import eel

_engine = pyttsx3.init('sapi5')
_voices = _engine.getProperty('voices')
_engine.setProperty('rate', 174)

def speak(text):
    text = str(text)
    try:
        if len(_voices) > 2:
            _engine.setProperty('voice', _voices[2].id)
        try:
            eel.DisplayMessage(text)
        except Exception:
            pass
        _engine.say(text)
        _engine.runAndWait()
        try:
            eel.receiverText(text)
        except Exception:
            pass
    except Exception:
        pass

# Expose the Python function to JavaScript

def takecommand():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("I'm listening...")
            try:
                eel.DisplayMessage("I'm listening...")
            except Exception:
                pass
            r.pause_threshold = 1
            try:
                r.adjust_for_ambient_noise(source)
            except Exception:
                pass
            audio = r.listen(source, timeout=10, phrase_time_limit=8)
    except Exception as e:
        print(f"Microphone error: {str(e)}\n")
        return None

    try:
        print("Recognizing...")
        try:
            eel.DisplayMessage("Recognizing...")
        except Exception:
            pass
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}\n")
        try:
            eel.DisplayMessage(query)
        except Exception:
            pass
        speak(query)
    except Exception as e:
        print(f"Error: {str(e)}\n")
        return None

    return query.lower()



@eel.expose
def takeAllCommands(message=None):
    if message is None:
        query = takecommand()  # If no message is passed, listen for voice input
        if not query:
            return  # Exit if no query is received
        print(query)
        eel.senderText(query)
    else:
        query = message  # If there's a message, use it
        print(f"Message received: {query}")
        eel.senderText(query)
    
    try:
        if query:
            if "open" in query:
                from backend.feature import openCommand
                openCommand(query)
            elif "send message" in query or "call" in query or "video call" in query:
                from backend.feature import findContact, whatsApp
                flag = ""
                Phone, name = findContact(query)
                if Phone != 0:
                    if "send message" in query:
                        flag = 'message'
                        speak("What message to send?")
                        query = takecommand()  # Ask for the message text
                    elif "call" in query:
                        flag = 'call'
                    else:
                        flag = 'video call'
                    whatsApp(Phone, query, flag, name)
            elif "on youtube" in query:
                from backend.feature import PlayYoutube
                PlayYoutube(query)
            else:
                from backend.feature import chatBot
                chatBot(query)
        else:
            speak("No command was given.")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("Sorry, something went wrong.")
    
    eel.ShowHood()
