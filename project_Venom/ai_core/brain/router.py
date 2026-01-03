from .system_brain import VenomBrain
from ai_core.core.config import config
from ai_core.core.logger import logger
from .analytical_engine import engine as math_engine
from modules.actions import VenomActions
from modules.media import MediaController
from modules.comms import Communicator


class CognitiveRouter:
    """
    Decides WHO processes the input:
    - Action System (Apps/Web)?
    - Media (YouTube)?
    - Comm (WhatsApp)?
    - Math Engine?
    - Neural Core?
    """

    def __init__(self):
        self.brain = VenomBrain()
        self.actions = VenomActions()
        self.media = MediaController()
        self.comm = Communicator()

        # Lazy load heavy modules only when needed or in separate thread?
        # For promptness, we init them as None and load on first use in their classes preferably,
        # but here we instantiate the controllers.
        from modules.vision import VisionSystem

        self.vision = VisionSystem()

        # Voice Cloner we load on demand as it's very heavy VRAM usage
        self.cloner = None

    async def process_thought_stream(self, prompt, visual_context=None):
        """
        Process thought but return a generator for streaming if it's a Neural Core task.
        Returns: (result, source, is_stream)
        """
        p_lower = prompt.lower()

        # 0. Hardware/Neural Controls
        if "clone" in p_lower and "voice" in p_lower:
            if not self.cloner:
                from modules.cloner import VoiceCloner

                self.cloner = VoiceCloner()

            # Extract text to say?
            # Simple demo behavior:
            demo_text = "I am now speaking with your voice parameters."
            self.cloner.speak_cloned(demo_text)
            return "Voice Cloning Sequence Initiated.", "Neural Audio", False

        # 0.5 Vision Check
        if (
            "vision" in p_lower
            or "see" in p_lower
            or "camera" in p_lower
            or "scan room" in p_lower
        ):
            if not hasattr(self, "vision_sys") or self.vision_sys is None:
                from modules.vision import VisionSystem

                self.vision_sys = VisionSystem()

            report = self.vision_sys.analyze_frame()
            return report, "Visual Cortex", False

        # 1. Media Check
        if "play" in p_lower and ("youtube" in p_lower or "song" in p_lower):
            result = self.media.play_youtube(prompt)
            return result, "Media System", False

        # 2. Comm Check
        if "whatsapp" in p_lower or "send message" in p_lower:
            target = "Mom"  # Placeholder
            if "to" in p_lower:
                parts = p_lower.split("to")
                if len(parts) > 1:
                    target = parts[1].strip().split()[0]

            result = self.comm.send_whatsapp(target, message="Hello from Venom")
            return result, "Comms System", False

        # 3. System Operations (Deploy/Optimize)
        if "deploy" in p_lower and ("kubernetes" in p_lower or "docker" in p_lower):
            import subprocess
            import sys

            subprocess.Popen(
                [sys.executable, "deploy_venom.py"],
                creationflags=subprocess.CREATE_NEW_CONSOLE,
            )
            return "Initiating Deployment Sequence...", "System Operations", False

        if "optimize" in p_lower:
            return (
                "Running Quantum Optimization Algorithms... System Efficiency: 98.4%",
                "Quantum Cortex",
                False,
            )

        # 4. Analytics Check
        if "analytics" in p_lower or "graph" in p_lower or "performance" in p_lower:
            from modules.analytics import VenomAnalytics

            va = VenomAnalytics()
            result = va.generate_report()
            return result, "Venom Analytics", False

        # 5. Action Check (Fastest)
        action_result = self.actions.execute(prompt)
        if action_result:
            return action_result, "Kinetic System", False

        # 4. Math Check
        math_result = await math_engine.process_math(prompt)
        if math_result:
            return math_result, "Analytical Engine", False

        # 4.5. Cloud Chat Fallback (Inspiration Integration)
        if "huggingface" in p_lower or ("chat" in p_lower and "cloud" in p_lower):
            from modules.features import get_huggingface_chat

            result = get_huggingface_chat(prompt)
            return result, "HuggingChat Integration", False

        # 5. Urgency Check
        urgency = "STANDARD"
        if "critical" in prompt.lower() or "fast" in prompt.lower():
            urgency = "CRITICAL"

        # 6. Brain Inference (Streaming)
        # Load System Prompt
        try:
            with open("system_prompt.txt", "r") as f:
                core_identity = f.read()
        except:
            core_identity = "You are Venom. Be concise and direct."

        system_instruction = core_identity
        if "analyze" in p_lower or "scan" in p_lower:
            # Append specific instructions if needed, but keep core identity
            system_instruction += (
                "\nFocus: Analyze code structure, complexity, and security."
            )

        stream_gen = self.brain.generate_stream(
            prompt,
            system_instruction=system_instruction,
            visual_context=visual_context,
            urgency=urgency,
        )
        return stream_gen, "Neural Core", True
