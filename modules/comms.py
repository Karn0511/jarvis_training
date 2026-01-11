"""Communications module for WhatsApp and messaging."""

import os
import sqlite3
import subprocess
import time
from urllib.parse import quote

from ai_core.core.logger import logger

try:
    import pyautogui

    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False


class Communicator:
    """
    Handles WhatsApp and Communications (Calls/Messages).
    Using Protocol Buffers/URI Text Injection.
    """

    def __init__(self):
        # We might need a database for contacts if we want 'findContact'
        # For now, let's keep it simple or allow direct numbering
        self.db_path = "data/contacts.db"
        self._init_db()

    def _init_db(self):
        os.makedirs("data", exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS contacts
                     (name text, phone text)"""
        )
        # Seed some data if empty?
        conn.commit()
        conn.close()

    def add_contact(self, name, phone):
        """Add a contact to the database."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO contacts VALUES (?, ?)", (name, phone))
        conn.commit()
        conn.close()
        return f"Added {name} to contacts."

    def find_contact(self, name_query):
        """Find a contact by name query."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "SELECT phone FROM contacts WHERE name LIKE ?", ("%" + name_query + "%",)
        )
        result = c.fetchone()
        conn.close()
        return result[0] if result else None

    def send_whatsapp(self, target, message=None, action="message"):
        """
        Action: 'message', 'call', 'videocall'
        Target: Name or Phone
        """
        phone = self.find_contact(target)
        if not phone:
            # Assume target is phone if not found?
            if any(char.isdigit() for char in target):
                phone = target
            else:
                return f"Contact '{target}' not found."

        if not phone.startswith("+"):
            # building it for India default based on logs, but should be generic
            if not phone.startswith("91") and len(phone) == 10:
                phone = "+91" + phone
            elif not phone.startswith("+"):
                phone = "+" + phone

        encoded_msg = quote(message) if message else ""
        whatsapp_url = f"whatsapp://send?phone={phone}&text={encoded_msg}"

        # Trigger URL
        full_command = f'start "" "{whatsapp_url}"'
        try:
            result = subprocess.run(full_command, shell=True, check=False)
            if result.returncode != 0:
                logger.error(
                    f"Failed to open WhatsApp: return code {result.returncode}"
                )
        except Exception as e:
            logger.error(f"Failed to open WhatsApp: {e}")
            return f"Error opening WhatsApp: {e}"

        time.sleep(2)  # Wait for app launch

        # Automation for message send if available
        if action == "message" and message and PYAUTOGUI_AVAILABLE:
            time.sleep(1)
            pyautogui.press("enter")
            return f"Message sent to {target}."

        return f"WhatsApp opened for {target}."
