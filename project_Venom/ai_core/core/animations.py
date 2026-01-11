
"""
Advanced Terminal Animations for Jarvis CLI
Beautiful, responsive animations using rich
"""

import time
import random
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.live import Live
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box
from rich.style import Style

console = Console()

# The VENOM Banner
VENOM_TEXT = """
██╗   ██╗███████╗███╗   ███╗ ██████╗ ███╗   ███╗
██║   ██║██╔════╝████╗ ████║██╔═══██╗████╗ ████║
██║   ██║█████╗  ██╔████╔██║██║   ██║██╔████╔██║
╚██╗ ██╔╝██╔══╝  ██║╚██╔╝██║██║   ██║██║╚██╔╝██║
 ╚████╔╝ ███████╗██║ ╚═╝ ██║╚██████╔╝██║ ╚═╝ ██║
  ╚═══╝  ╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝     ╚═╝
"""

BRAIN_ANIMATION = ["🧠", "🤔", "💭", "✨", "🚀"]

def show_banner():
    """Display advanced animated Venom + Jarvis banner with simulated gradient"""
    console.clear()
    
    # 1. Advanced Boot Log
    boot_steps = [
        ("INITIALIZING KERNEL", "red"),
        ("LOADING NEURAL WEIGHTS", "magenta"),
        ("SYNCING QUANTUM STATES", "blue"),
        ("CONNECTING TO GRID", "cyan"),
        ("SYSTEM ONLINE", "green"),
    ]
    
    with Progress(
        SpinnerColumn(spinner_name="dots12"),
        TextColumn("[bold {task.fields[color]}]{task.description}"),
        BarColumn(bar_width=40, complete_style="green", finished_style="green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
        transient=True
    ) as progress:
        for desc, color in boot_steps:
            task = progress.add_task(f"[{color}]{desc}...", total=100, color=color)
            axis = 10
            while not progress.finished:
                progress.update(task, advance=axis)
                axis += 5
                time.sleep(0.04)
                if progress.tasks[0].completed >= 100:
                    break
            time.sleep(0.1)

    # 2. Gradient Banner Display
    # Rich doesn't do true gradients easily, so we mimic it with row-by-row color shifts
    console.clear()
    gradient_colors = [
        "bright_red", "red", "magenta", "violet", "blue", "cyan", "bright_cyan"
    ]
    
    lines = VENOM_TEXT.strip().split("\n")
    
    # Animate Banner Entrance
    for i, line in enumerate(lines):
        color = gradient_colors[i % len(gradient_colors)]
        console.print(Align.center(f"[{color}]{line}[/{color}]"))
        time.sleep(0.1)
    
    # Subtitles
    subtitle = Text("\nADVANCED SYMBIOTIC INTELLIGENCE", style="bold white")
    console.print(Align.center(subtitle))
    
    info = Text("Powered by Gemini 1.5 & Venom Core", style="dim white")
    console.print(Align.center(info))
    print("\n")

def connection_animation():
    """Simulate connection to mainframes"""
    # Simply a spinner for 'Connecting'
    with console.status("[bold cyan]Establishing Secure Uplink...[/bold cyan]", spinner="earth"):
        time.sleep(1.5)
    console.print("[bold green]✔ Secure Uplink Established.[/bold green]")



def thinking_animation(message: str = "Processing", duration: float = 2.0):
    """Show engaged quantum thinking animation"""
    start_time = time.time()
    colors = ["cyan", "blue", "magenta", "violet"]
    
    with Live(console=console, refresh_per_second=12) as live:
        i = 0
        while time.time() - start_time < duration:
            emoji = BRAIN_ANIMATION[i % len(BRAIN_ANIMATION)]
            color = colors[i % len(colors)]
            
            # Quantum Spinner
            spinner = "|/-\\"[i % 4]
            
            content = Table.grid()
            content.add_column()
            content.add_row(Align.center(f"[bold {color}]{spinner} {emoji} {message}...[/bold {color}]"))
            
            live.update(Panel(content, border_style=color, box=box.HEAVY_EDGE, width=50, padding=(0,1)))
            time.sleep(0.1)
            i += 1



def rainbow_text(text: str, delay: float = 0.05):
    """Display text in rainbow colors"""
    colors = ["red", "yellow", "green", "cyan", "blue", "magenta"]
    
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        console.print(char, style=f"bold {color}", end="")
        time.sleep(delay)
    console.print()


def code_analysis_animation():
    """Specific animation for code analysis"""
    stages = [
        ("🔍 Scanning code structure", 1.0),
        ("🧬 Analyzing complexity", 1.2),
        ("🔬 Detecting patterns", 1.0),
        ("⚡ Running quantum analysis", 1.5),
        ("✨ Generating insights", 1.0),
    ]
    
    with Progress(
        SpinnerColumn(spinner_name="dots12", style="bold cyan"),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(complete_style="cyan"),
        TextColumn("[cyan]{task.percentage:>3.0f}%"),
        console=console,
        transient=False
    ) as progress:
        
        for stage, duration in stages:
            task = progress.add_task(stage, total=100)
            steps = 20
            for i in range(steps):
                progress.update(task, advance=100/steps)
                time.sleep(duration / steps)
            progress.update(task, completed=100)


async def ai_response_stream(text_generator, title="Venom Architecture"):
    """
    Stream AI response.
    """
    output = ""
    title_text = f"🤖 {title}"
    
    # Initial empty panel
    live_panel = Panel(
        "",
        title=title_text,
        border_style="cyan",
        box=box.ROUNDED,
        padding=(1, 2)
    )
    
    with Live(live_panel, console=console, refresh_per_second=15, vertical_overflow="visible") as live:
        if isinstance(text_generator, str):
            # Simulation (Fallback)
            chunk_size = 4
            for i in range(0, len(text_generator), chunk_size):
                output += text_generator[i:i+chunk_size]
                live.update(Panel(output, title=title_text, border_style="cyan", box=box.ROUNDED, padding=(1, 2)))
                await asyncio.sleep(0.01)
        else:
            # Async Generator (Real)
            try:
                start_time = time.time()
                async for chunk in text_generator:
                    if chunk:
                        output += chunk
                        live.update(Panel(output, title=title_text, border_style="cyan", box=box.ROUNDED, padding=(1, 2)))
                
                # If response was empty
                if not output:
                    output = "..."
                    live.update(Panel(output, title=title_text, border_style="red", box=box.ROUNDED, padding=(1, 2)))

            except Exception as e:
                output += f"\n[bold red](Stream Interrupted: {e})[/bold red]"
                live.update(Panel(output, title=title_text, border_style="red", box=box.ROUNDED, padding=(1, 2)))
    
    return output


def matrix_effect(lines: int = 20, duration: float = 3.0):
    """Matrix-style falling code effect with cascading binary rain"""
    height = console.height or 24
    width = console.width or 80
    
    # Pre-generate some random columns
    columns = [random.randint(0, height) for _ in range(width)]
    
    start_time = time.time()
    with Live(console=console, refresh_per_second=20, auto_refresh=False) as live:
        while time.time() - start_time < duration:
            table = Table.grid(padding=0)
            for _ in range(width):
                table.add_column()
            
            # Generate frame
            rows = []
            for y in range(height):
                row = []
                for x in range(width):
                    # Logic for rain
                    if columns[x] > y:
                        char = random.choice("0123456789ABCDEF") # Hex/Binary matrix
                        style = "green"
                        if columns[x] == y + 1:
                            style = "bold bright_white" # Head
                        elif columns[x] == y + 2:
                            style = "bold bright_green"
                        elif columns[x] - y > 15: # Tail fade
                            char = " "
                            
                        # Random stutter
                        if random.random() < 0.05:
                            char = random.choice("01")
                            
                        row.append(Text(char, style=style))
                    else:
                        row.append(Text(" "))
                rows.append(row)
            
            # Build Grid
            for row_data in rows:
                table.add_row(*row_data)
            
            live.update(table)
            live.refresh()
            
            # Advance columns
            for x in range(width):
                if random.random() < 0.1: # Move chance
                    columns[x] += 1
                    if columns[x] > height + 15: # Reset
                        columns[x] = random.randint(-15, 0)
            
            time.sleep(0.05)
    
    console.clear()


