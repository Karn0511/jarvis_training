"""Voice cloning module using Coqui TTS."""

import os
import time
import asyncio
from ai_core.core.logger import logger


class VoiceCloner:
    """
    Voice Cloning Module using Coqui TTS.
    Note: Requires 'TTS' package. On Python 3.13 this is often incompatible.
    This module safely degrades if TTS is not available.
    """

    def __init__(self):
        self.enabled = False
        try:
            from TTS.api import TTS

            # Init TTS with a multi-speaker model
            # This downloads the model on first run (~1GB)
            self.model = TTS(
                model_name="tts_models/multilingual/multi-dataset/your_tts",
                progress_bar=False,
                gpu=True,
            )
            self.enabled = True
            logger.organ("VOICE_CLONE", "Coqui TTS Model Loaded (GPU Enabled)")
        except ImportError:
            logger.error("Coqui TTS ('TTS') not installed. Voice Cloning Disabled.")
            logger.info("To enable: Use Python 3.10 and run: pip install TTS")
        except Exception as e:
            logger.error(f"Voice Clone Init Failed: {e}")

    def speak_cloned(self, text, speaker_wav="user_voice.wav", language="en"):
        """
        Synthesize speech using a reference audio file (cloning).
        """
        if not self.enabled:
            logger.error("Voice Clone functionality unavailable.")
            return

        output_file = "venom_output.wav"
        try:
            # Check if reference voice exists
            if not os.path.exists(speaker_wav):
                # Fallback or create dummy if testing?
                # For now just log
                logger.error(f"Reference voice file '{speaker_wav}' not found.")
                return

            self.model.tts_to_file(
                text=text,
                speaker_wav=speaker_wav,
                language=language,
                file_path=output_file,
            )

            # Play Audio
            # We use a simple player or default system player
            # Using pygame mixer from existing setup could work but let's use a quick sounddevice/pydub/os
            # Simplest: os.startfile in detached thread
            import winsound

            winsound.PlaySound(output_file, winsound.SND_FILENAME)

        except Exception as e:
            logger.error(f"Cloning Synthesis Failed: {e}")


if __name__ == "__main__":
    v = VoiceCloner()

