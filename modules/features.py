import os
import webbrowser
import time
import subprocess
import requests
from pathlib import Path
from ai_core.core.logger import logger


def play_youtube(query: str):
    """Play a video on YouTube based on the query."""
    try:
        import pywhatkit as kit

        search_term = query.replace("play", "").replace("on youtube", "").strip()
        logger.info(f"Playing on YouTube: {search_term}")
        kit.playonyt(search_term)
        return f"Playing {search_term} on YouTube."
    except Exception as e:
        logger.error(f"YouTube Error: {e}")
        return str(e)


def open_app(app_name: str):
    """Open a system application or website."""
    app_name = app_name.lower().strip()

    # Common mappings
    common_apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": "chrome.exe",
        "spotify": "spotify.exe",
    }

    if app_name in common_apps:
        try:
            subprocess.Popen(common_apps[app_name])
            return f"Opening {app_name}..."
        except FileNotFoundError:
            pass

    # Web fallback
    if "." in app_name:  # Simple heuristic for URLs
        if not app_name.startswith("http"):
            url = "https://" + app_name
        else:
            url = app_name
        webbrowser.open(url)
        return f"Opening website {url}..."

    # OS Start fallback
    try:
        if os.name == "nt":
            os.system(f"start {app_name}")
        else:
            subprocess.Popen(app_name, shell=True)
        return f"Attempting to launch {app_name}..."
    except Exception as e:
        return f"Failed to allow launch: {e}"


def get_huggingface_chat(query: str):
    """Fallback chat using HuggingChat if configured."""
    try:
        from hugchat import hugchat

        cookie_path = Path(
            "storage/cookie.json"
        )  # Updated to match Project Venom structure
        if cookie_path.exists():
            chatbot = hugchat.ChatBot(cookie_path=str(cookie_path))
            cid = chatbot.new_conversation()
            chatbot.change_conversation(cid)
            return str(chatbot.chat(query))
        else:
            return "HuggingChat cookie not found."
    except Exception as e:
        return f"HuggingChat Error: {e}"
