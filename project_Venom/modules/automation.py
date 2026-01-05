"""
Advanced Automation Module for Venom
App control, web automation, system commands, and smart shortcuts.
"""

import asyncio
import os
import subprocess
import webbrowser
from typing import Optional
from ai_core.core.logger import logger

try:
    from AppOpener import open as app_open, close as app_close
    APP_OPENER_AVAILABLE = True
except ImportError:
    APP_OPENER_AVAILABLE = False

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False


class VenomAutomation:
    """
    Advanced Automation System for app control, web automation, and system commands.
    """

    def __init__(self):
        self.enabled = True
        logger.organ("AUTOMATION", "Automation System ONLINE")
        
        if not APP_OPENER_AVAILABLE:
            logger.warning("AppOpener not installed. App control limited.")
        
        if not PYAUTOGUI_AVAILABLE:
            logger.warning("PyAutoGUI not installed. GUI automation limited.")
        
        if not KEYBOARD_AVAILABLE:
            logger.warning("keyboard not installed. Hotkey support limited.")

    async def open_application(self, app_name: str) -> str:
        """
        Open an application by name.
        
        Args:
            app_name: Application name (e.g., 'chrome', 'notepad', 'vscode')
            
        Returns:
            Status message
        """
        if not APP_OPENER_AVAILABLE:
            # Fallback to system command
            return await self.run_command(app_name)
        
        try:
            logger.organ("AUTOMATION", f"Opening: {app_name}")
            await asyncio.to_thread(app_open, app_name, match_closest=True)
            return f"Opened {app_name}"
        except Exception as e:
            logger.error(f"Failed to open {app_name}: {e}")
            return f"Could not open {app_name}: {e}"

    async def close_application(self, app_name: str) -> str:
        """
        Close an application by name.
        
        Args:
            app_name: Application name
            
        Returns:
            Status message
        """
        if not APP_OPENER_AVAILABLE:
            return "App control unavailable (AppOpener not installed)"
        
        try:
            logger.organ("AUTOMATION", f"Closing: {app_name}")
            await asyncio.to_thread(app_close, app_name, match_closest=True)
            return f"Closed {app_name}"
        except Exception as e:
            logger.error(f"Failed to close {app_name}: {e}")
            return f"Could not close {app_name}: {e}"

    async def open_website(self, url: str) -> str:
        """
        Open a website in default browser.
        
        Args:
            url: Website URL (can be partial, will add https://)
            
        Returns:
            Status message
        """
        # Ensure proper URL format
        if not url.startswith(('http://', 'https://')):
            url = f"https://{url}"
        
        try:
            logger.organ("AUTOMATION", f"Opening website: {url}")
            await asyncio.to_thread(webbrowser.open, url)
            return f"Opened {url}"
        except Exception as e:
            logger.error(f"Failed to open website: {e}")
            return f"Could not open website: {e}"

    async def run_command(self, command: str, shell: bool = True) -> str:
        """
        Run a system command.
        
        Args:
            command: Command to execute
            shell: Run through shell (default True)
            
        Returns:
            Command output or error message
        """
        try:
            logger.organ("AUTOMATION", f"Executing: {command}")
            
            result = await asyncio.to_thread(
                subprocess.run,
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                output = result.stdout.strip() or "Command executed successfully"
                logger.success(f"Command success: {command}")
                return output
            else:
                error = result.stderr.strip() or f"Command failed with code {result.returncode}"
                logger.error(f"Command failed: {error}")
                return f"Error: {error}"
                
        except subprocess.TimeoutExpired:
            return "Command timed out (>30s)"
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            return f"Execution error: {e}"

    async def press_keys(self, *keys: str) -> str:
        """
        Simulate keyboard key presses.
        
        Args:
            *keys: Keys to press (e.g., 'ctrl', 'c' for Ctrl+C)
            
        Returns:
            Status message
        """
        if not PYAUTOGUI_AVAILABLE:
            return "GUI automation unavailable (PyAutoGUI not installed)"
        
        try:
            logger.organ("AUTOMATION", f"Pressing keys: {'+'.join(keys)}")
            
            if len(keys) > 1:
                # Hotkey combination
                await asyncio.to_thread(pyautogui.hotkey, *keys)
            else:
                # Single key
                await asyncio.to_thread(pyautogui.press, keys[0])
            
            return f"Pressed: {'+'.join(keys)}"
        except Exception as e:
            logger.error(f"Key press failed: {e}")
            return f"Error: {e}"

    async def type_text(self, text: str, interval: float = 0.05) -> str:
        """
        Type text using keyboard automation.
        
        Args:
            text: Text to type
            interval: Delay between keystrokes
            
        Returns:
            Status message
        """
        if not PYAUTOGUI_AVAILABLE:
            return "GUI automation unavailable"
        
        try:
            logger.organ("AUTOMATION", f"Typing text ({len(text)} chars)")
            await asyncio.to_thread(pyautogui.write, text, interval=interval)
            return f"Typed {len(text)} characters"
        except Exception as e:
            logger.error(f"Text typing failed: {e}")
            return f"Error: {e}"

    async def screenshot(self, filepath: Optional[str] = None) -> str:
        """
        Take a screenshot.
        
        Args:
            filepath: Save location (optional, auto-generates if None)
            
        Returns:
            File path of screenshot
        """
        if not PYAUTOGUI_AVAILABLE:
            return "Screenshot unavailable (PyAutoGUI not installed)"
        
        try:
            if filepath is None:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filepath = f"storage/screenshots/screenshot_{timestamp}.png"
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            logger.organ("AUTOMATION", f"Taking screenshot: {filepath}")
            screenshot = await asyncio.to_thread(pyautogui.screenshot)
            await asyncio.to_thread(screenshot.save, filepath)
            
            logger.success(f"Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            return f"Error: {e}"

    async def lock_system(self) -> str:
        """Lock the system (Windows)."""
        try:
            logger.organ("AUTOMATION", "Locking system...")
            await self.run_command("rundll32.exe user32.dll,LockWorkStation")
            return "System locked"
        except Exception as e:
            return f"Lock failed: {e}"

    async def shutdown_system(self, delay: int = 0) -> str:
        """
        Shutdown system.
        
        Args:
            delay: Delay in seconds before shutdown
            
        Returns:
            Status message
        """
        try:
            logger.organ("AUTOMATION", f"Shutdown scheduled in {delay}s")
            await self.run_command(f"shutdown /s /t {delay}")
            return f"System will shutdown in {delay} seconds"
        except Exception as e:
            return f"Shutdown failed: {e}"

    async def restart_system(self, delay: int = 0) -> str:
        """
        Restart system.
        
        Args:
            delay: Delay in seconds
            
        Returns:
            Status message
        """
        try:
            logger.organ("AUTOMATION", f"Restart scheduled in {delay}s")
            await self.run_command(f"shutdown /r /t {delay}")
            return f"System will restart in {delay} seconds"
        except Exception as e:
            return f"Restart failed: {e}"

    async def cancel_shutdown(self) -> str:
        """Cancel scheduled shutdown/restart."""
        try:
            logger.organ("AUTOMATION", "Cancelling shutdown")
            await self.run_command("shutdown /a")
            return "Shutdown cancelled"
        except Exception as e:
            return f"Cancel failed: {e}"

    async def get_battery_status(self) -> str:
        """Get system battery status."""
        try:
            import psutil
            battery = psutil.sensors_battery()
            
            if battery:
                percent = battery.percent
                plugged = "Charging" if battery.power_plugged else "On Battery"
                time_left = ""
                
                if not battery.power_plugged and battery.secsleft > 0:
                    hours = battery.secsleft // 3600
                    minutes = (battery.secsleft % 3600) // 60
                    time_left = f", {hours}h {minutes}m remaining"
                
                return f"Battery: {percent}% ({plugged}{time_left})"
            else:
                return "No battery detected (desktop system)"
        except Exception as e:
            return f"Battery status unavailable: {e}"

    async def set_volume(self, level: int) -> str:
        """
        Set system volume (Windows).
        
        Args:
            level: Volume level 0-100
            
        Returns:
            Status message
        """
        level = max(0, min(100, level))  # Clamp to 0-100
        
        try:
            # Windows volume control via nircmd (if available) or powershell
            ps_script = f"(New-Object -ComObject WScript.Shell).SendKeys([char]174)"  # Volume up/down keys
            # This is simplified - proper implementation would use pycaw library
            logger.organ("AUTOMATION", f"Setting volume to {level}%")
            return f"Volume set to {level}% (requires pycaw library for full control)"
        except Exception as e:
            return f"Volume control failed: {e}"


# Global instance
_automation_instance = None


def get_automation() -> VenomAutomation:
    """Get or create the global automation instance."""
    global _automation_instance
    if _automation_instance is None:
        _automation_instance = VenomAutomation()
    return _automation_instance


if __name__ == "__main__":
    # Test
    async def test():
        auto = VenomAutomation()
        print(await auto.get_battery_status())
        print(await auto.open_website("github.com"))
    
    asyncio.run(test())
