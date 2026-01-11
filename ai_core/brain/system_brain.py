import os
import asyncio
import warnings
import json
import aiohttp

warnings.filterwarnings("ignore")

import google.generativeai as genai
from ai_core.core.config import config
from ai_core.core.logger import logger


class VenomBrain:
    """
    Unified Neural Core v2.1.
    Robust Streaming & Fallback Architecture.
    """

    def __init__(self):
        logger.system("Initializing Advanced Neural Core...")

        self.api_key = config.GEMINI_API_KEY
        self.client_active = False

        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.client_active = True
            except Exception as e:
                logger.error(f"Brain Init Failed: {e}")

        # Models
        self.models = {"fast": [config.FAST_MODEL], "smart": [config.SMART_MODEL]}

    async def generate_stream(
        self, prompt, system_instruction="", visual_context=None, urgency="STANDARD"
    ):
        """
        Robust streaming Generator.
        """
        # 1. Cloud Attempt
        if self.client_active:
            candidates = (
                self.models["smart"] if urgency == "CRITICAL" else self.models["fast"]
            )

            # Construct Prompt Safely
            full_contents = []
            if visual_context:
                full_contents.append(f"CONTEXT: {visual_context}")

            full_contents.append(prompt)

            # Fix: Ensure non-empty
            if not prompt or not prompt.strip():
                yield "I cannot process empty thoughts."
                return

            for model_name in candidates:
                try:
                    model = genai.GenerativeModel(
                        model_name,
                        system_instruction=(
                            system_instruction if system_instruction else None
                        ),
                    )

                    # Ensure contents is a list, expected by V1
                    response_stream = await model.generate_content_async(
                        contents=full_contents,
                        generation_config=genai.types.GenerationConfig(temperature=0.7),
                        stream=True,
                    )

                    async for chunk in response_stream:
                        if chunk.text:
                            yield chunk.text
                    return  # Success

                except Exception as e:
                    logger.warning(f"Cloud Synapse {model_name} failed: {e}")
                    continue

        # 2. Local Fallback (Ollama)
        # Yield a small indicator so user knows we switched
        # yield "[Switched to Local Bio-Link] "

        try:
            local_url = "http://localhost:11434/api/generate"
            payload = {
                "model": "phi3",  # Try phi3 first
                "prompt": f"System: {system_instruction}\nUser: {prompt}",
                "stream": True,
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(local_url, json=payload) as resp:
                    if resp.status == 200:
                        async for line in resp.content:
                            if line:
                                try:
                                    data = json.loads(line)
                                    if "response" in data:
                                        yield data["response"]
                                    if data.get("done"):
                                        break
                                except:
                                    pass
                        return
                    else:
                        # Try llama3 if phi3 fails? Or just fail.
                        pass

        except Exception as e:
            # logger.error(f"Local Link Failed: {e}")
            pass

        yield "My mind is foggy. (Cloud & Local Brains Unreachable)."
        yield "\nPlease ensure 'GEMINI_API_KEY' is valid or Ollama is running."

    async def generate_response(self, prompt, **kwargs):
        """Non-streaming wrapper"""
        full_text = ""
        async for chunk in self.generate_stream(prompt, **kwargs):
            full_text += chunk
        return full_text
