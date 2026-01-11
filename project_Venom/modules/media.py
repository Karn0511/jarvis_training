"""Media controller for YouTube and streaming."""

import re

from ai_core.core.logger import logger

try:
    import pywhatkit as kit

    PYWHATKIT_AVAILABLE = True
except ImportError:
    PYWHATKIT_AVAILABLE = False
    kit = None


class MediaController:
    """
    Handles streaming/media commands (YouTube, etc.).
    """

    def __init__(self):
        """Initialize media controller."""
        self.available = PYWHATKIT_AVAILABLE

    def extract_yt_term(self, command):
        """Extract YouTube search term from command."""
        # Improved regex to catch "play X on youtube" or "on youtube play X" or just "play X"
        pattern = r"(?:play\s+)(.*?)(?:\s+on\s+youtube)"
        match = re.search(pattern, command, re.IGNORECASE)
        if match:
            return match.group(1)

        # Fallback if "on youtube" isn't explicitly there but implied by router
        if "play" in command:
            return command.replace("play", "").replace("on youtube", "").strip()
        return None

    def play_youtube(self, query):
        """Play video on YouTube."""
        if not PYWHATKIT_AVAILABLE:
            return "YouTube playback not available (pywhatkit not installed)"
        search_term = self.extract_yt_term(query)
        if search_term:
            logger.info(f"Playing on YouTube: {search_term}")
            try:
                kit.playonyt(search_term)
                return f"Streaming {search_term} on YouTube..."
            except Exception as e:
                logger.error(f"YouTube playback failed: {e}")
                return f"Failed to play: {e}"
        else:
            return "Could not identify what to play."
