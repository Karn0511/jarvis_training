"""
Advanced Image Generation Module for Venom
Integrates Hugging Face Stable Diffusion XL and local image management.
"""

import asyncio
import os
from random import randint
from PIL import Image
import requests
from ai_core.core.logger import logger
from ai_core.core.config import config


class VenomImageGenerator:
    """
    Advanced Image Generation System using Stable Diffusion XL.
    Generates high-quality 4K images with multiple variations.
    """

    def __init__(self):
        self.api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        self.output_folder = "storage/generated_images"
        os.makedirs(self.output_folder, exist_ok=True)

        # Get API key from environment
        self.api_key = os.getenv("HUGGINGFACE_API_KEY", "")
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

        if not self.api_key:
            logger.warning("HuggingFace API Key not set. Image generation may fail.")
            logger.info("Set HUGGINGFACE_API_KEY in .env file")

        self.enabled = bool(self.api_key)
        logger.organ(
            "IMAGE_GEN",
            f"Image Generator {'ONLINE' if self.enabled else 'OFFLINE (No API Key)'}",
        )

    async def _query_api(self, payload: dict) -> bytes:
        """Send async query to Hugging Face API."""
        try:
            response = await asyncio.to_thread(
                requests.post,
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=60,
            )
            if response.status_code == 200:
                return response.content
            else:
                logger.error(
                    f"API returned status {response.status_code}: {response.text}"
                )
                return b""
        except Exception as e:
            logger.error(f"Image API query failed: {e}")
            return b""

    async def generate_images(self, prompt: str, count: int = 4) -> list[str]:
        """
        Generate multiple images from prompt.

        Args:
            prompt: Text description of desired image
            count: Number of variations to generate (default 4)

        Returns:
            List of file paths to generated images
        """
        if not self.enabled:
            return []

        logger.organ("IMAGE_GEN", f"Generating {count} images for: {prompt}")

        # Create enhanced prompt for quality
        enhanced_prompt = (
            f"{prompt}, quality=4K, sharpness=maximum, "
            f"Ultra High details, high resolution, professional lighting"
        )

        # Create concurrent tasks for parallel generation
        tasks = []
        for i in range(count):
            payload = {
                "inputs": f"{enhanced_prompt}, seed={randint(0, 1000000)}",
                "options": {"wait_for_model": True},
            }
            task = asyncio.create_task(self._query_api(payload))
            tasks.append(task)

        # Wait for all images
        logger.info(f"Processing {count} image generation tasks...")
        results = await asyncio.gather(*tasks)

        # Save images
        saved_files = []
        safe_prompt = prompt.replace(" ", "-")[:50]  # Limit filename length

        for i, image_bytes in enumerate(results, 1):
            if image_bytes:
                filename = f"{safe_prompt}-{i}.jpg"
                filepath = os.path.join(self.output_folder, filename)

                try:
                    # Save image
                    with open(filepath, "wb") as f:
                        f.write(image_bytes)

                    saved_files.append(filepath)
                    logger.success(f"Image {i}/{count} saved: {filename}")
                except Exception as e:
                    logger.error(f"Failed to save image {i}: {e}")

        if saved_files:
            logger.organ(
                "IMAGE_GEN", f"Generated {len(saved_files)} images successfully"
            )
        else:
            logger.error("No images were generated successfully")

        return saved_files

    async def display_images(self, image_paths: list[str]):
        """
        Display generated images using default system viewer.

        Args:
            image_paths: List of file paths to display
        """
        if not image_paths:
            logger.warning("No images to display")
            return

        logger.organ("IMAGE_GEN", f"Displaying {len(image_paths)} images")

        for path in image_paths:
            try:
                img = Image.open(path)
                img.show()
                await asyncio.sleep(1)  # Delay between images
            except Exception as e:
                logger.error(f"Failed to display {path}: {e}")

    async def generate_and_display(self, prompt: str, count: int = 4):
        """
        Generate images and display them.

        Args:
            prompt: Text description
            count: Number of images to generate

        Returns:
            Success message
        """
        if not self.enabled:
            return "Image generation unavailable. Please set HUGGINGFACE_API_KEY."

        # Generate
        image_paths = await self.generate_images(prompt, count)

        if not image_paths:
            return "Image generation failed. Check API key and network connection."

        # Display
        await self.display_images(image_paths)

        return f"Generated and displayed {len(image_paths)} images for: {prompt}"

    def list_generated_images(self) -> list[str]:
        """List all previously generated images."""
        try:
            files = os.listdir(self.output_folder)
            image_files = [f for f in files if f.endswith((".jpg", ".png", ".jpeg"))]
            return sorted(
                image_files,
                key=lambda x: os.path.getmtime(os.path.join(self.output_folder, x)),
                reverse=True,
            )
        except Exception as e:
            logger.error(f"Failed to list images: {e}")
            return []

    def get_recent_images(self, limit: int = 10) -> list[str]:
        """Get most recently generated images."""
        all_images = self.list_generated_images()
        return all_images[:limit]


# Global instance (lazy loaded)
_image_gen_instance = None


def get_image_generator() -> VenomImageGenerator:
    """Get or create the global image generator instance."""
    global _image_gen_instance
    if _image_gen_instance is None:
        _image_gen_instance = VenomImageGenerator()
    return _image_gen_instance


if __name__ == "__main__":
    # Test the module
    async def test():
        gen = VenomImageGenerator()
        result = await gen.generate_and_display(
            "futuristic cyberpunk city at night", count=2
        )
        print(result)

    asyncio.run(test())
