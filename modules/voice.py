"""Voice synthesis module using Edge TTS."""

import os
import asyncio
import edge_tts

# Suppress Pygame Welcome
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

from ai_core.core.config import config
from ai_core.core.logger import logger


class VenomVoice:
    """
    The Mouth of Venom.
    Uses Microsoft Edge's Neural TTS (Free, High Quality).
    """

    def __init__(self, voice="en-US-ChristopherNeural"):
        self.voice = voice
        self.output_file = os.path.join(config.DATA_DIR, "speech_buffer.mp3")

        # Init Audio Engine
        try:
            pygame.mixer.init()
            logger.success("Vocal Cord (Edge-TTS) Initialized")
        except Exception as e:
            logger.error(f"Audio Engine Init Failed: {e}")

    async def speak(self, text):
        """
        Synthesizes text to speech and plays it.
        """
        if not text or not config.VOICE_ENABLED:
            return

        try:
            # Generate Audio File
            communicate = edge_tts.Communicate(text, self.voice)
            await communicate.save(self.output_file)

            # Play Audio
            self._play_audio_file()

        except Exception as e:
            logger.error(f"Speech Synthesis Failed: {e}")

    def _play_audio_file(self):
        try:
            # Load and Play
            pygame.mixer.music.load(self.output_file)
            pygame.mixer.music.play()

            # Wait for finish (blocking, but okay for speech flow usually)
            # For highly async, we might want to check is_busy in a loop
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            # Unload to allow overwrite
            pygame.mixer.music.unload()
        except Exception as e:
            logger.error(f"Playback Failed: {e}")

    def set_voice(self, voice_name):
        self.voice = voice_name
