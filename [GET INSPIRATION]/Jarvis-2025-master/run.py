import multiprocessing
import os
import sys
import time

def _tui_enabled():
    return os.getenv("JARVIS_TUI", "1") == "1" and sys.stdout.isatty()

def splash():
    if not _tui_enabled():
        return
    logo = [
        "",
        "  ███╗   ██╗ █████╗ ██████╗ ██╗██╗   ██╗███████╗",
        "  ████╗  ██║██╔══██╗██╔══██╗██║██║   ██║██╔════╝",
        "  ██╔██╗ ██║███████║██████╔╝██║██║   ██║█████╗  ",
        "  ██║╚██╗██║██╔══██║██╔══██╗██║╚██╗ ██╔╝██╔══╝  ",
        "  ██║ ╚████║██║  ██║██║  ██║██║ ╚████╔╝ ███████╗",
        "  ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝",
        "",
        "                Jarvis Assistant starting...",
        "",
    ]
    for line in logo:
        print(line)
    spinner = ["-", "\\", "|", "/"]
    end_time = time.time() + 1.5
    i = 0
    while time.time() < end_time:
        sys.stdout.write("\rInitializing " + spinner[i % len(spinner)])
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\rInitializing done \n")
    sys.stdout.flush()

def startJarvis():
    print ("Process 1 Starting...")
    from main import start
    start()
    
def listenHotword():
    print ("Process 2 Starting...")
    from backend.feature import hotword
    hotword()
    
if __name__ == "__main__":
    splash()
    print("Starting process...")
    process1 = multiprocessing.Process(target=startJarvis)
    process1.start()
    print("Jarvis PID:", process1.pid)
    start_hotword = os.getenv("JARVIS_HOTWORD", "0") == "1" and os.getenv("PORCUPINE_ACCESS_KEY")
    process2 = None
    if start_hotword:
        process2 = multiprocessing.Process(target=listenHotword)
        process2.start()
        print("Hotword PID:", process2.pid)
    process1.join()
    if process2 and process2.is_alive():
        process2.terminate()
        print("Hotword terminated.")
        process2.join()
    print("System is terminated.")
def _tui_enabled():
    return os.getenv("JARVIS_TUI", "1") == "1" and sys.stdout.isatty()

def splash():
    if not _tui_enabled():
        return
    logo = [
        "",
        "  ███╗   ██╗ █████╗ ██████╗ ██╗██╗   ██╗███████╗",
        "  ████╗  ██║██╔══██╗██╔══██╗██║██║   ██║██╔════╝",
        "  ██╔██╗ ██║███████║██████╔╝██║██║   ██║█████╗  ",
        "  ██║╚██╗██║██╔══██║██╔══██╗██║╚██╗ ██╔╝██╔══╝  ",
        "  ██║ ╚████║██║  ██║██║  ██║██║ ╚████╔╝ ███████╗",
        "  ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝",
        "",
        "                Jarvis Assistant starting...",
        "",
    ]
    for line in logo:
        print(line)
    spinner = ["-", "\\", "|", "/"]
    end_time = time.time() + 1.5
    i = 0
    while time.time() < end_time:
        sys.stdout.write("\rInitializing " + spinner[i % len(spinner)])
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write("\rInitializing done \n")
    sys.stdout.flush()