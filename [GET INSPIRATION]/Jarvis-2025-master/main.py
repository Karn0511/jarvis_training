import os
import sys
import time
from backend.feature import openCommand, findContact, whatsApp, PlayYoutube, chatBot, play_assistant_sound
from backend.command import speak
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.spinner import Spinner
    _rich_available = True
    _console = Console()
except Exception:
    _rich_available = False
    _console = None



def start():
    
    def _tui_enabled():
        return os.getenv("JARVIS_TUI", "1") == "1" and sys.stdout.isatty()

    def print_status(msg):
        if _tui_enabled():
            print(msg)

    def spinner(msg, duration=1.0):
        if not _tui_enabled():
            return
        frames = ["-", "\\", "|", "/"]
        end = time.time() + duration
        i = 0
        sys.stdout.write(msg + " ")
        sys.stdout.flush()
        while time.time() < end:
            sys.stdout.write("\r" + msg + " " + frames[i % len(frames)])
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        sys.stdout.write("\r" + msg + " done \n")
        sys.stdout.flush()

    def typewrite(msg, delay=0.02):
        s = msg
        for ch in s:
            sys.stdout.write(ch)
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write("\n")
        sys.stdout.flush()

    def banner(text):
        if _rich_available and os.getenv("JARVIS_TUI_STYLE", "basic") == "rich":
            _console.print(Panel.fit(text, border_style="cyan", style="bold magenta"))
        else:
            typewrite(text)

    banner("Initializing Jarvis terminal mode...")
    spinner("Starting", duration=1.0)
    play_assistant_sound()
    speak("Welcome to Jarvis")
    typewrite("Type a command. Ctrl+C to exit.")
    while True:
        try:
            if _rich_available and os.getenv("JARVIS_TUI_STYLE", "basic") == "rich":
                _console.print("[bold cyan]>[/] ", end="")
            typed = input().strip()
        except Exception:
            typed = ""
        query = typed.lower()
        if not query:
            continue
        if _rich_available and os.getenv("JARVIS_TUI_STYLE", "basic") == "rich":
            with _console.status("Processing...", spinner="dots"):
                pass
        if "exit" in query or "quit" in query or "stop" in query:
            speak("Goodbye")
            break
        if "open" in query:
            openCommand(query)
        elif "send message" in query or "call" in query or "video call" in query:
            flag = ""
            Phone, name = findContact(query)
            if Phone != 0:
                if "send message" in query:
                    flag = 'message'
                    speak("What message to send?")
                    m = takecommand()
                    if m:
                        whatsApp(Phone, m, flag, name)
                elif "call" in query:
                    flag = 'call'
                    whatsApp(Phone, "", flag, name)
                else:
                    flag = 'video call'
                    whatsApp(Phone, "", flag, name)
        elif "on youtube" in query:
            PlayYoutube(query)
        else:
            chatBot(query)

