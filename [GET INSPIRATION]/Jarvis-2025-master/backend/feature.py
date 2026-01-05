# import playsound
# import eel


# @eel.expose
# def playAssistantSound():
#     music_dir = "frontend\\assets\\audio\\start_sound.mp3"
#     playsound(music_dir)


from compileall import compile_path
from pathlib import Path
import os
import re
from shlex import quote
import struct
import subprocess
import time
import webbrowser
import eel
from hugchat import hugchat 
import pvporcupine
import pyaudio
import pyautogui
import pywhatkit as kit
import pygame
import requests
from openai import OpenAI
from backend.command import speak
from backend.config import ASSISTANT_NAME
import sqlite3

from backend.helper import extract_yt_term, remove_words
conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()
_mixer_ready = False
def _ensure_mixer():
    global _mixer_ready
    if _mixer_ready:
        return
    try:
        pygame.mixer.init()
        _mixer_ready = True
    except Exception:
        _mixer_ready = False

# Define the function to play sound
@eel.expose
def play_assistant_sound():
    base = Path(__file__).resolve().parents[1]
    sound_path = base / "frontend" / "assets" / "audio" / "start_sound.mp3"
    _ensure_mixer()
    if _mixer_ready:
        pygame.mixer.music.load(str(sound_path))
        pygame.mixer.music.play()
    
    
def openCommand(query):
    query = query.replace(ASSISTANT_NAME,"")
    query = query.replace("open","")
    query.lower()
    
    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute( 
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")


def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)


def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        access_key = os.getenv("PORCUPINE_ACCESS_KEY")
        if not access_key:
            print("Porcupine access key not set. Hotword disabled.")
            return
        porcupine = pvporcupine.create(access_key=access_key, keywords=["jarvis", "alexa"]) 
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
            keyword_index = porcupine.process(keyword)
            if keyword_index >= 0:
                print("hotword detected")
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT Phone FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    
    
def whatsApp(Phone, message, flag, name):
    

    if flag == 'message':
        target_tab = 12
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={Phone}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)


def get_chat_response(query):
    provider = os.getenv("JARVIS_CHAT_PROVIDER", "hugchat").lower()
    if provider == "openai":
        try:
            client = OpenAI()
            resp = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[{"role": "user", "content": query}],
                temperature=0.7,
            )
            return resp.choices[0].message.content
        except Exception as e:
            return "OpenAI error: " + str(e)
    if provider == "ollama":
        host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        model = os.getenv("OLLAMA_MODEL", "llama3.2")
        try:
            r = requests.post(host + "/api/generate", json={"model": model, "prompt": query})
            if r.ok:
                data = r.json()
                return data.get("response", "")
            return "Ollama error: " + r.text
        except Exception as e:
            return "Ollama error: " + str(e)
    base = Path(__file__).resolve().parents[1]
    cookie_path = base / "backend" / "cookie.json"
    try:
        chatbot = hugchat.ChatBot(cookie_path=str(cookie_path))
        cid = chatbot.new_conversation()
        chatbot.change_conversation(cid)
        return str(chatbot.chat(query.lower()))
    except Exception as e:
        return "Chat error: " + str(e)

def chatBot(query):
    response = get_chat_response(query)
    print(response)
    speak(response)
    return response