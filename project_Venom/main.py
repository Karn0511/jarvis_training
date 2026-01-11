import asyncio
import sys
import os

# Force UTF-8 encoding for Windows console
if sys.platform == "win32":
    import codecs

    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from ai_core.core.logger import logger
from ai_core.core.event_bus import bus
from ai_core.core.kernel import VenomKernel
from ai_core.brain.router import CognitiveRouter
from modules.voice import VenomVoice
from ai_core.core.synapse import synapse
from ai_core.core.neural_viz import visualizer
from ai_core.core.config import POLL_RATE
from ai_core.core.animations import (
    show_banner,
    thinking_animation,
    ai_response_stream,
    matrix_effect,
    connection_animation,
    code_analysis_animation,
)

console = Console()


async def interactive_loop():
    """Main interactive loop for the Venom system."""
    # 1. Advanced Startup Sequence
    show_banner()
    connection_animation()

    logger.print("BOOTING VENOM: ADVANCED ARCHITECTURE", style="system")
    synapse.broadcast("BOOTING", "Kernel initialization started...")

    # Initialize Core
    kernel = VenomKernel()

    # CUDA Check
    try:
        import torch

        if torch.cuda.is_available():
            logger.success(
                f"CUDA ACCELERATION ENABLED: {torch.cuda.get_device_name(0)}"
            )
            synapse.broadcast(
                "HARDWARE", f"CUDA Enabled: {torch.cuda.get_device_name(0)}"
            )
    except Exception:
        pass

    router = CognitiveRouter()
    voice = VenomVoice()

    # Start Kernel Background Tasks
    kernel_task = asyncio.create_task(kernel.start())
    await asyncio.sleep(0.5)

    # Status Broadcast
    synapse.broadcast(
        "ONLINE", "System Ready. Waiting for Neural Link...", synapse.get_vitals()
    )
    await voice.speak("Venom System Online.")

    # Detection of Headless / Docker Mode
    is_headless = not sys.stdin.isatty() or os.environ.get("VENOM_WEB_MODE") == "true"
    if is_headless:
        logger.system("WEB CONTROL MODE ACTIVE: Syncing with Frontend Dashboard.")

    while True:
        try:
            user_input = None

            # Phase 2: Visualize LISTENING state
            vitals = synapse.get_vitals()
            visualizer.generate_frame("EARS", 0.3, float(vitals.get("cpu_percent", 0)))

            # 1. Check for Web Command (Synapse)
            web_cmd = synapse.get_input()
            if web_cmd:
                user_input = web_cmd
                console.print(
                    f"\n[bold magenta]>> WEB SIGNAL RECEIVED: {user_input}[/bold magenta]"
                )

            # 2. Console Input (Only if not in headless mode)
            if not user_input:
                if not is_headless:
                    try:
                        synapse.broadcast("LISTENING", "Waiting for input...", vitals)
                        user_input = Prompt.ask(
                            "\n[bold cyan]KARN[/bold cyan]",
                            default="",
                            show_default=False,
                        )
                    except EOFError:
                        break
                else:
                    # In headless mode, we just wait for web signals
                    synapse.broadcast("LISTENING", "Monitoring web signals...", vitals)
                    await asyncio.sleep(POLL_RATE)
                    continue

            if not user_input or not user_input.strip():
                continue

            if user_input.lower() in ["exit", "shutdown", "quit"]:
                await voice.speak("Shutting down system.")
                synapse.broadcast("OFFLINE", "System Shutdown")
                break

            if not user_input.strip():
                continue

            # Secret Easter Eggs
            if user_input.lower() == "matrix":
                matrix_effect()
                continue

            if user_input.lower() == "clear":
                console.clear()
                continue

            # Phase 2: Visualize PROCESSING state
            vitals = synapse.get_vitals()
            vitals["active_node"] = "QUANTUM_GATE"
            vitals["intensity"] = 0.7
            synapse.broadcast("PROCESSING", f"Input: {user_input}", vitals)
            visualizer.generate_frame(
                "QUANTUM_GATE", 0.7, float(vitals.get("cpu_percent", 0))
            )

            # 3. Process via Cognitive Router
            # Determine if this involves code analysis for specialized animation
            is_analysis = (
                "analyze" in user_input.lower() or "scan" in user_input.lower()
            )

            response, source, is_stream = await router.process_thought_stream(
                user_input
            )

            final_text_response = ""

            # Phase 2: Visualize THINKING state (LLM Core active)
            vitals = synapse.get_vitals()
            vitals["active_node"] = "LLM_CORE"
            vitals["intensity"] = 0.9
            synapse.broadcast("THINKING", f"Active Module: {source}", vitals)
            visualizer.generate_frame(
                "LLM_CORE", 0.9, float(vitals.get("cpu_percent", 0))
            )

            # 4. Animated Output
            if is_stream:
                if is_analysis:
                    code_analysis_animation()
                else:
                    thinking_animation()

                # Stream the response
                final_text_response = await ai_response_stream(response, title=source)

            else:
                # Static response (Math/Actions)
                final_text_response = response

                color = "green" if source == "Analytical Engine" else "white"
                border = "green" if source == "Analytical Engine" else "cyan"

                console.print(
                    Panel(
                        str(final_text_response),
                        title=f"[bold {color}]{source}[/bold {color}]",
                        border_style=border,
                    )
                )

            # Phase 2: Visualize RESPONSE state
            vitals = synapse.get_vitals()
            vitals["active_node"] = "MEMORY"
            vitals["intensity"] = 0.6
            synapse.broadcast("RESPONSE", f"Output generated by {source}", vitals)
            visualizer.generate_frame(
                "MEMORY", 0.6, float(vitals.get("cpu_percent", 0))
            )

            # 5. Voice Synthesis
            if final_text_response and len(str(final_text_response)) < 300:
                # Don't read out massive code blocks provided by analysis
                # Phase 2: Visualize VOICE state
                vitals = synapse.get_vitals()
                vitals["active_node"] = "VOICE"
                vitals["intensity"] = 0.7
                visualizer.generate_frame(
                    "VOICE", 0.7, float(vitals.get("cpu_percent", 0))
                )
                await voice.speak(str(final_text_response))

        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.error(f"Runtime Exception: {e}")
            synapse.broadcast("ERROR", str(e))
            console.print_exception()

    await bus.emit("SHUTDOWN")
    logger.system("System processing terminated.")


if __name__ == "__main__":
    try:
        asyncio.run(interactive_loop())
    except KeyboardInterrupt:
        logger.system("Emergency Halt Triggered.")
    except Exception as e:
        logger.error(f"Critical System Failure: {e}")
