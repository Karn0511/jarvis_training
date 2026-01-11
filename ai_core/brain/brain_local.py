
import aiohttp
import json
from ai_core.core.logger import logger
from ai_core.core.config import config

class LocalBrain:
    """
    Interface for Local LLM (e.g., Ollama or LlamaCPP).
    Optimized for RTX 3050 (4GB VRAM) - assumes quantized models.
    """
    def __init__(self, model_name="phi3", base_url="http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.generate_endpoint = f"{base_url}/api/generate"
        self.chat_endpoint = f"{base_url}/api/chat"
        # self.check_connection()

    async def think(self, prompt, context="", stream=False):
        """
        Generates a thought using the local model.
        """
        full_prompt = f"Context: {context}\nUser: {prompt}\nVenom:"
        
        payload = {
            "model": self.model_name,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_ctx": 4096
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.generate_endpoint, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("response", "")
                    else:
                        logger.error(f"Local Brain Error {response.status}: {await response.text()}")
                        return None
        except Exception as e:
            logger.error(f"Local Brain Connection Failed: {e}")
            return None

    def check_connection(self):
        # Implementation for health check
        pass


