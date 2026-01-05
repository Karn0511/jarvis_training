"""
Advanced Terminal Animations for Jarvis CLI
Beautiful, responsive animations using rich
"""

import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.live import Live
from rich.table import Table
from rich.text import Text
from rich.layout import Layout
from rich.align import Align
from rich import box
from rich.style import Style
import random

console = Console()

# Cool ASCII Art for Jarvis
JARVIS_ASCII = """
     ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗
     ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝
     ██║███████║██████╔╝██║   ██║██║███████╗
██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║
╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║
 ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝
"""

BRAIN_ANIMATION = ["🧠", "🤔", "💭", "✨", "🚀"]
ROBOT_ANIMATION = ["🤖", "⚙️", "🔧", "⚡", "💡"]
LOADING_CHARS = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]


def show_banner():
    """Display animated Jarvis banner"""
    console.clear()
    
    # Create gradient effect
    colors = ["cyan", "blue", "magenta", "blue", "cyan"]
    
    for i, line in enumerate(JARVIS_ASCII.split('\n')):
        color = colors[i % len(colors)]
        console.print(line, style=f"bold {color}", justify="center")
        time.sleep(0.05)
    
    console.print("\n[bold cyan]Advanced AI Coding Assistant[/bold cyan]", justify="center")
    console.print("[dim]Powered by Multi-AI Routing & Quantum Intelligence[/dim]\n", justify="center")


def typing_effect(text: str, style: str = "bold cyan", delay: float = 0.03):
    """Simulate typing effect"""
    output = ""
    with Live(console=console, refresh_per_second=30) as live:
        for char in text:
            output += char
            live.update(Text(output, style=style))
            time.sleep(delay)
    console.print()


def pulse_text(text: str, duration: float = 2.0, style: str = "bold cyan"):
    """Create pulsing text effect"""
    styles = [
        "dim cyan",
        "cyan",
        "bold cyan",
        "bold bright_cyan",
        "bold cyan",
        "cyan",
    ]
    
    start_time = time.time()
    with Live(console=console, refresh_per_second=20) as live:
        while time.time() - start_time < duration:
            for s in styles:
                if time.time() - start_time >= duration:
                    break
                live.update(Align.center(Text(text, style=s)))
                time.sleep(0.1)


def progress_bar_animation(message: str, total: int = 100, style: str = "cyan"):
    """Show progress bar with custom styling"""
    with Progress(
        SpinnerColumn(spinner_name="dots"),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(complete_style=style, finished_style="bold green"),
        TextColumn("[bold cyan]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
        transient=False
    ) as progress:
        task = progress.add_task(message, total=total)
        for i in range(total):
            progress.update(task, advance=1)
            time.sleep(0.02)


def matrix_effect(lines: int = 20, duration: float = 3.0):
    """Matrix-style falling code effect with cascading binary rain"""
    height = max(10, lines)
    available_width = max(10, console.width - 4)
    width = min(100, available_width)
    binary_chars = "01"
    extra_chars = "23456789ABCDEF@$%&*"

    def pick_char() -> str:
        return random.choice(binary_chars) if random.random() < 0.85 else random.choice(extra_chars)

    drops = [
        {
            "y": random.randint(-height, 0),
            "velocity": random.uniform(0.35, 0.95),
            "tail": random.randint(max(4, height // 3), height),
            "tick": 0.0,
        }
        for _ in range(width)
    ]

    console.clear()
    start_time = time.time()
    with Live(console=console, refresh_per_second=30) as live:
        while time.time() - start_time < duration:
            rows = []
            for row_index in range(height):
                row_text = Text()
                for drop in drops:
                    head = drop["y"]
                    tail_start = head - drop["tail"]
                    char = " "
                    style = "dim green"

                    if row_index == head:
                        char = pick_char()
                        style = "bold bright_white"
                    elif tail_start <= row_index < head:
                        char = pick_char()
                        depth = (row_index - tail_start) / max(drop["tail"], 1)
                        if depth < 0.3:
                            style = "bold bright_green"
                        elif depth < 0.7:
                            style = "green"
                        else:
                            style = "dim green"
                    elif random.random() < 0.01:
                        char = random.choice(binary_chars)
                        style = "dim green"

                    row_text.append(char, style=style)
                rows.append(row_text)

            table = Table.grid(padding=0)
            table.add_column(width=width, no_wrap=True)
            for row_text in rows:
                table.add_row(row_text)
            live.update(Align.center(table))

            for drop in drops:
                drop["tick"] += drop["velocity"]
                while drop["tick"] >= 1:
                    drop["y"] += 1
                    drop["tick"] -= 1
                if drop["y"] - drop["tail"] > height:
                    drop["y"] = random.randint(-height // 2, 0)
                    drop["tail"] = random.randint(max(4, height // 3), height)
                    drop["velocity"] = random.uniform(0.35, 0.95)

            time.sleep(0.05)


def thinking_animation(message: str = "Thinking", duration: float = 2.0):
    """Show thinking animation with brain emojis"""
    with Live(console=console, refresh_per_second=10) as live:
        start_time = time.time()
        i = 0
        while time.time() - start_time < duration:
            emoji = BRAIN_ANIMATION[i % len(BRAIN_ANIMATION)]
            dots = "." * ((i % 3) + 1)
            text = Text()
            text.append(f"{emoji} ", style="bold yellow")
            text.append(f"{message}{dots}", style="bold cyan")
            live.update(Align.center(text))
            time.sleep(0.3)
            i += 1


def processing_animation(message: str = "Processing", duration: float = 2.0):
    """Show processing animation"""
    with Progress(
        SpinnerColumn(spinner_name="arc", style="bold magenta"),
        TextColumn("[bold cyan]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task(message, total=None)
        time.sleep(duration)


def success_animation(message: str):
    """Show success message with animation"""
    success_box = Panel(
        Align.center(f"✨ {message} ✨"),
        border_style="bold green",
        box=box.DOUBLE_EDGE,
        padding=(1, 2)
    )
    
    # Flash effect
    for _ in range(3):
        console.print(success_box)
        time.sleep(0.15)
        console.clear()
        time.sleep(0.1)
    
    console.print(success_box)


def error_animation(message: str):
    """Show error message with animation"""
    error_box = Panel(
        Align.center(f"❌ {message}"),
        border_style="bold red",
        box=box.HEAVY,
        padding=(1, 2)
    )
    
    # Shake effect
    for i in range(5):
        offset = " " * (i % 2)
        console.print(offset + str(error_box))
        time.sleep(0.1)
        if i < 4:
            console.clear()


def loading_spinner(message: str = "Loading", duration: float = 2.0):
    """Custom loading spinner"""
    with Live(console=console, refresh_per_second=20) as live:
        start_time = time.time()
        i = 0
        while time.time() - start_time < duration:
            spinner = LOADING_CHARS[i % len(LOADING_CHARS)]
            text = Text()
            text.append(f"{spinner} ", style="bold yellow")
            text.append(message, style="bold blue")
            live.update(text)
            time.sleep(0.08)
            i += 1


def create_stats_table(data: dict) -> Table:
    """Create animated stats table"""
    table = Table(
        show_header=True,
        header_style="bold magenta",
        border_style="cyan",
        box=box.ROUNDED,
        title="📊 System Statistics",
        title_style="bold cyan"
    )
    
    table.add_column("Metric", style="dim cyan", width=20)
    table.add_column("Value", style="bold yellow", width=30)
    table.add_column("Status", justify="center", width=10)
    
    for key, value in data.items():
        status = "✅" if value else "❌"
        table.add_row(key, str(value), status)
    
    return table


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
            for i in range(100):
                progress.update(task, advance=1)
                time.sleep(duration / 100)
            progress.update(task, completed=100)


def ai_response_stream(text: str, style: str = "bold cyan"):
    """Simulate AI streaming response"""
    words = text.split()
    output = ""
    
    panel = Panel(
        "",
        title="🤖 Jarvis Response",
        border_style="blue",
        box=box.ROUNDED
    )
    
    with Live(panel, console=console, refresh_per_second=30) as live:
        for word in words:
            output += word + " "
            updated_panel = Panel(
                output,
                title="🤖 Jarvis Response",
                border_style="blue",
                box=box.ROUNDED,
                padding=(1, 2)
            )
            live.update(updated_panel)
            time.sleep(0.05)


def connection_animation():
    """Show connecting to backend animation"""
    with Progress(
        SpinnerColumn(spinner_name="aesthetic", style="bold cyan"),
        TextColumn("[bold blue]Connecting to Jarvis Backend..."),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("connect", total=None)
        time.sleep(2)


def quantum_analysis_effect():
    """Special quantum computing effect"""
    qubits = ["│0⟩", "│1⟩", "│+⟩", "│-⟩"]
    
    with Live(console=console, refresh_per_second=20) as live:
        for _ in range(20):
            text = Text()
            text.append("⚛️  Quantum Circuit: ", style="bold magenta")
            for _ in range(8):
                text.append(f"{random.choice(qubits)} ", style="bold cyan")
            live.update(Align.center(text))
            time.sleep(0.1)
