
import asyncio
import random
import time
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.align import Align

console = Console()

class MatrixUI:
    """
    Advanced Terminal User Interface (TUI).
    Provides Matrix-style animations and structured layouts.
    """
    def __init__(self):
        self.console = console

    async def startup_sequence(self):
        """
        Runs the Hollywood-style boot sequence.
        """
        self.console.clear()
        
        # 1. Matrix Rain Effect (Simulated)
        chars = "0101010101VENOM010100101SYSTEM010101"
        for i in range(15):
            line = "".join(random.choice(chars) for _ in range(self.console.width))
            self.console.print(line, style="green dim")
            await asyncio.sleep(0.05)
            
        self.console.clear()
        self.console.print(Align.center("[bold green]PROJECT VENOM[/bold green]"))
        self.console.print(Align.center("[dim]System Architecture v3.0[/dim]"))
        self.console.print("\n")

        # 2. Loading Modules
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.percentage:>3.0f}%"),
            console=self.console,
            transient=True
        ) as progress:
            task1 = progress.add_task("[cyan]Initializing Quantum Core...", total=100)
            task2 = progress.add_task("[magenta]Syncing Neural Weights...", total=100)
            task3 = progress.add_task("[green]Connecting Senses...", total=100)
            
            while not progress.finished:
                progress.update(task1, advance=random.randint(1, 10))
                if progress.tasks[0].completed > 30:
                    progress.update(task2, advance=random.randint(1, 15))
                if progress.tasks[0].completed > 60:
                    progress.update(task3, advance=random.randint(1, 20))
                await asyncio.sleep(0.1)
                
        self.console.print("[bold green]✔ SYSTEM ONLINE[/bold green]")
        await asyncio.sleep(0.5)

    async def display_stream(self, stream_gen, source="VENOM", style="cyan"):
        """
        Streams AI response token by token in a panel.
        Returns the full text.
        """
        title_style = f"bold {style}"
        border_style = style
        
        text_buffer = ""
        # Create a Live display
        with Live(Panel("", title=f"[{title_style}]{source}[/{title_style}]", border_style=border_style, padding=(1, 2)), refresh_per_second=12, console=self.console) as live:
            async for chunk in stream_gen:
                text_buffer += chunk
                live.update(Panel(Text(text_buffer, justify="left"), title=f"[{title_style}]{source}[/{title_style}]", border_style=border_style, padding=(1, 2)))
        
        return text_buffer

    def display_output(self, text, source="VENOM", style="green"):
        """
        Displays AI response in a styled panel.
        """
        title_style = f"bold {style}"
        border_style = style
        
        panel = Panel(
            Text(text, justify="left"),
            title=f"[{title_style}]{source}[/{title_style}]",
            border_style=border_style,
            padding=(1, 2)
        )
        self.console.print(panel)

    def display_alert(self, text, level="INFO"):
        colors = {"INFO": "blue", "WARNING": "yellow", "CRITICAL": "red", "SUCCESS": "green"}
        color = colors.get(level, "white")
        self.console.print(f"[{color}][{level}][/] {text}")

ui = MatrixUI()


