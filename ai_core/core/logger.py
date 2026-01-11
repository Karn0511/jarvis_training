from rich.console import Console
from rich.theme import Theme
import sys

# Force UTF-8 encoding for Windows console
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, TypeError):
        pass

custom_theme = Theme(
    {
        "info": "dim cyan",
        "warning": "magenta",
        "error": "bold red",
        "critical": "bold white on red",
        "success": "bold green",
        "system": "bold blue",
        "brain": "bold #39FF14",
    }
)

console = Console(theme=custom_theme)


class VenomLogger:
    def print(self, text, style="info"):
        console.print(text, style=style)

    def success(self, text):
        self.print(f"[✔] {text}", style="success")

    def error(self, text):
        self.print(f"[✖] {text}", style="error")

    def system(self, text):
        self.print(f"[SYSTEM] {text}", style="system")

    def info(self, text):
        self.print(f"[INFO] {text}", style="info")

    def warning(self, text):
        self.print(f"[!] {text}", style="warning")

    def organ(self, name, text):
        self.print(f"[{name}] {text}", style="warning")


logger = VenomLogger()
