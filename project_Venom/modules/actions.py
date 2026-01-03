
import os
import webbrowser
import subprocess
import difflib
import datetime

class VenomActions:
    def __init__(self):
        print("Initializing Kinetic Output (Actions)...")
        # Common Windows Apps registry
        self.app_map = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "cmd": "cmd.exe",
            "explorer": "explorer.exe",
            "chrome": "chrome.exe",
            "edge": "msedge.exe",
            "code": "code",
            "spotify": "spotify.exe",
            "paint": "mspaint.exe",
            "settings": "start ms-settings:"
        }

    def execute(self, cmd_text):
        """
        Parses text to trigger real-world actions.
        Returns a response string if an action was taken, else None.
        """
        cmd = cmd_text.lower()
        
        # 1. Advanced System Ops
        if "lock pc" in cmd or "lock system" in cmd or "secure workstation" in cmd:
            import ctypes
            ctypes.windll.user32.LockWorkStation()
            return "Securing Protocol Initiated. System Locked."

        if "screenshot" in cmd or "capture screen" in cmd:
            try:
                import pyautogui
                save_dir = "./data/screenshots"
                os.makedirs(save_dir, exist_ok=True)
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{save_dir}/venom_snap_{timestamp}.png"
                pyautogui.screenshot(filename)
                subprocess.Popen(f'explorer /select,"{os.path.abspath(filename)}"')
                return f"Visual Log Captured: {filename}"
            except Exception as e:
                return f"Screenshot Failed: {e}"

        if "create file" in cmd or "make file" in cmd:
            try:
                name = cmd.replace("create file", "").replace("make file", "").strip()
                if not name: name = "venom_log.txt"
                with open(name, "w") as f:
                    f.write(f"CREATED BY VENOM @ {datetime.datetime.now()}")
                return f"Constructed file entity: {name}"
            except Exception as e:
                return f"Fabrication Error: {e}"

        # 2. Volume Control
        if "volume up" in cmd:
            try:
                import pyautogui
                for _ in range(5): pyautogui.press("volumeup")
                return "Audio Output Increased."
            except: pass
        if "volume down" in cmd:
            try:
                import pyautogui
                for _ in range(5): pyautogui.press("volumedown")
                return "Audio Output Decreased."
            except: pass
        if "mute" in cmd:
            try:
                import pyautogui
                pyautogui.press("volumemute")
                return "Audio Output Silenced."
            except: pass

        # 3. Web Search
        if "search for" in cmd or "google" in cmd:
            query = cmd.replace("search for", "").replace("google", "").strip()
            url = f"https://www.google.com/search?q={query}"
            webbrowser.open(url)
            return f"Opening search for: {query}"
        
        # 4. Open Website
        if "open" in cmd and ".com" in cmd:
            words = cmd.split()
            for word in words:
                if ".com" in word:
                    if not word.startswith("http"):
                        word = "https://" + word
                    webbrowser.open(word)
                    return f"Opening portal: {word}"
        
        # 5. Open App
        if "open" in cmd:
            app_name = cmd.replace("open", "").strip()
            # fuzzy match
            match = difflib.get_close_matches(app_name, self.app_map.keys(), n=1, cutoff=0.6)
            if match:
                target = self.app_map[match[0]]
                try:
                    subprocess.Popen(target, shell=True)
                    return f"Launching {match[0]}..."
                except Exception as e:
                    return f"Failed to launch {match[0]}: {e}"
            else:
                 try:
                     subprocess.Popen(app_name, shell=True)
                     return f"Attempting to launch {app_name}..."
                 except:
                     pass

        # 6. Global Pulse (News/Weather - Free)
        if "weather" in cmd:
             webbrowser.open("https://wttr.in")
             return "Accessing Global Atmosphere Data..."
        
        if "news" in cmd:
             webbrowser.open("https://news.google.com")
             return "Syncing with Human Information Streams..."

        return None

if __name__ == "__main__":
    act = VenomActions()
    print(act.execute("open calculator"))

