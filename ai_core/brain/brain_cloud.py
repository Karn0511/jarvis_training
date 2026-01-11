try:
    import google.generativeai as genai

    _HAS_GENAI = True
except ImportError:
    pass
    _HAS_GENAI = False

from ai_core.core.config import config
from ai_core.core.logger import logger


class CloudBrain:
    """
    Interface for Cloud Intelligence (Gemini Pro).
    Used for complex reasoning, coding, or when local brain is unsure.
    """

    def __init__(self):
        if not _HAS_GENAI:
            logger.error(
                "Create: `pip install google-generativeai` to enable Cloud Brain."
            )
            self.model = None
            return

        if not config.GEMINI_API_KEY:
            logger.error("Gemini API Key missing! Cloud Brain disabled.")
            self.model = None
            return

        try:
            genai.configure(api_key=config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(config.SMART_MODEL)
            self.chat = self.model.start_chat(history=[])
            logger.success("Cloud Brain (Gemini) Connected")
        except Exception as e:
            logger.error(f"Cloud Brain Init Failed: {e}")
            self.model = None

    async def think_complex(self, prompt, context=""):
        """
        Executes deep reasoning via Cloud.
        """
        if not self.model:
            return "Thinking capacity limited (No Cloud Connection)."

        full_message = f"SYSTEM_CONTEXT: {context}\nUSER_REQUEST: {prompt}"

        try:
            # Gemini async call (simulated async wrapper if needed, or native if supported)
            # The google-generativeai lib is synchronous by default, wrapping in executor recommended for production.
            # For simplicity in this step, we run sync (blocking) but note it for future optimization.
            response = self.model.generate_content(full_message)
            return response.text
        except Exception as e:
            logger.error(f"Cloud Thought Failed: {e}")
            return None
