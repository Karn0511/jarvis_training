"""
Local LLM Model Handler
Supports Llama, Mistral, and other local models via Ollama or llama.cpp
"""

import asyncio
from typing import Optional, Dict, Any, AsyncGenerator
import json

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


class LocalLLMModel:
    """
    Local LLM model handler with fallback support
    """

    def __init__(self, model_name: str = "llama2", backend: str = "ollama"):
        """
        Initialize local LLM
        
        Args:
            model_name: Name of the model (llama2, mistral, codellama, etc.)
            backend: Backend to use (ollama, llamacpp)
        """
        self.model_name = model_name
        self.backend = backend
        self.available = self._check_availability()

    def _check_availability(self) -> bool:
        """Check if local model is available"""
        if self.backend == "ollama":
            return OLLAMA_AVAILABLE
        return False

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        Generate text from local LLM
        
        Args:
            prompt: User prompt
            system_prompt: System instruction
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        if not self.available:
            return self._fallback_response(prompt)

        if self.backend == "ollama":
            return await self._generate_ollama(prompt, system_prompt, temperature)
        
        return self._fallback_response(prompt)

    async def _generate_ollama(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float
    ) -> str:
        """Generate using Ollama"""
        try:
            messages = []
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            messages.append({
                "role": "user",
                "content": prompt
            })

            response = await asyncio.to_thread(
                ollama.chat,
                model=self.model_name,
                messages=messages,
                options={"temperature": temperature}
            )

            return response['message']['content']

        except Exception as e:
            print(f"⚠️  Ollama generation failed: {e}")
            return self._fallback_response(prompt)

    async def stream_generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """
        Stream generation from local LLM
        
        Args:
            prompt: User prompt
            system_prompt: System instruction
            
        Yields:
            Text chunks
        """
        if not self.available:
            yield self._fallback_response(prompt)
            return

        if self.backend == "ollama":
            async for chunk in self._stream_ollama(prompt, system_prompt):
                yield chunk

    async def _stream_ollama(
        self,
        prompt: str,
        system_prompt: Optional[str]
    ) -> AsyncGenerator[str, None]:
        """Stream from Ollama"""
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            stream = await asyncio.to_thread(
                ollama.chat,
                model=self.model_name,
                messages=messages,
                stream=True
            )

            for chunk in stream:
                if 'message' in chunk and 'content' in chunk['message']:
                    yield chunk['message']['content']

        except Exception as e:
            print(f"⚠️  Ollama streaming failed: {e}")
            yield self._fallback_response(prompt)

    def _fallback_response(self, prompt: str) -> str:
        """Generate fallback response when model unavailable"""
        return (
            f"[Local Model Unavailable]\n\n"
            f"Your query: {prompt[:100]}...\n\n"
            f"To use local LLM:\n"
            f"1. Install Ollama: https://ollama.ai\n"
            f"2. Pull model: ollama pull {self.model_name}\n"
            f"3. Restart Jarvis backend\n"
        )

    async def get_embeddings(self, text: str) -> list:
        """
        Get embeddings for text
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector
        """
        if not self.available or self.backend != "ollama":
            return []

        try:
            response = await asyncio.to_thread(
                ollama.embeddings,
                model=self.model_name,
                prompt=text
            )
            return response['embedding']
        except Exception as e:
            print(f"⚠️  Embedding generation failed: {e}")
            return []

    def get_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "model_name": self.model_name,
            "backend": self.backend,
            "available": self.available,
            "features": {
                "generation": self.available,
                "streaming": self.available,
                "embeddings": self.available and self.backend == "ollama"
            }
        }


# Default instance
default_model = LocalLLMModel()
