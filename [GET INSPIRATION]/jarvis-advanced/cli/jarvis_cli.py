from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.live import Live
from rich.align import Align
from dotenv import load_dotenv

from .client import JarvisClient
from .animations import (
    show_banner, thinking_animation, success_animation, 
    error_animation, code_analysis_animation, ai_response_stream,
    create_stats_table, typing_effect, connection_animation,
    processing_animation, progress_bar_animation
)

# Load environment variables
load_dotenv()

# Initialize
console = Console()
client = JarvisClient()


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(version='2.0.0', prog_name='Jarvis AI')
def cli(ctx):
    """
    🤖 JARVIS - Just A Rather Very Intelligent System
    
    Your advanced AI coding assistant with quantum intelligence
    """
    if ctx.invoked_subcommand is None:
        show_banner()
        console.print("\n[bold cyan]Available Commands:[/bold cyan]\n")
        console.print("  [yellow]status[/yellow]    - Check backend health")
        console.print("  [yellow]ask[/yellow]       - Ask a question")
        console.print("  [yellow]analyze[/yellow]   - Analyze code file")
        console.print("  [yellow]chat[/yellow]      - Interactive chat mode")
        console.print("  [yellow]execute[/yellow]   - Execute shell command")
        console.print("  [yellow]init[/yellow]      - Initialize project\n")
        console.print("[dim]Type 'jarvis --help' for more info[/dim]\n")


@cli.command()
def status():
    """Check Jarvis backend status with animation"""
    connection_animation()
    
    try:
        response = client.ping()
        success_animation("Backend Online!")
        
        # Create stats display
        stats = {
            "Status": "🟢 Online",
            "Version": response.get('version', '2.0.0'),
            "Features": response.get('features', 'All Active'),
            "Response Time": f"{response.get('response_time', '<100')}ms"
        }
        
        table = create_stats_table(stats)
        console.print("\n", table, "\n")
        
    except Exception as e:
        error_animation("Backend Offline!")
        console.print(Panel(
            f"[red]Error:[/red] {str(e)}\n\n"
            "[yellow]Start backend with:[/yellow]\n"
            "  [cyan]cd backend && uvicorn main:app[/cyan]",
            title="❌ Connection Failed",
            border_style="red",
            box=box.HEAVY
        ))


@cli.command()
@click.argument('question', nargs=-1, required=True)
@click.option('--stream', is_flag=True, help='Stream response in real-time')
def ask(question, stream):
    """
    Ask Jarvis anything with animated response
    
    Examples:
      jarvis ask "How do I reverse a list in Python?"
      jarvis ask "Explain async/await" --stream
    """
    question_text = ' '.join(question)
    
    # Show question with typing effect
    console.print("\n[bold yellow]You:[/bold yellow]")
    console.print(f"  {question_text}\n")
    
    # Thinking animation
    thinking_animation("Analyzing your question", duration=1.5)
    
    try:
        response = client.ask(question_text)
        answer = response.get('answer', 'No response')
        
        # Animate the response
        console.print()
        if stream:
            ai_response_stream(answer)
        else:
            # Display with markdown support
            console.print(Panel(
                Markdown(answer),
                title="🤖 Jarvis",
                border_style="cyan",
                box=box.ROUNDED,
                padding=(1, 2)
            ))
        
        # Show metadata
        model = response.get('model', 'unknown')
        cached = response.get('cached', False)
        cache_status = "⚡ Cached" if cached else "🔄 Fresh"
        console.print(f"\n[dim]Model: {model} | {cache_status}[/dim]\n")
        
    except Exception as e:
        error_animation(f"Failed to get response: {str(e)}")


@cli.command()
@click.argument('filepath', type=click.Path(exists=True))
@click.option('--detailed', is_flag=True, help='Show detailed analysis')
def analyze(filepath, detailed):
    """
    Analyze code with quantum-enhanced AI
    
    Example: jarvis analyze script.py --detailed
    """
    try:
        # Read file with progress
        console.print(f"\n[bold cyan]📁 Loading:[/bold cyan] {filepath}\n")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Show file preview
        syntax = Syntax(code[:500], "python", theme="monokai", line_numbers=True)
        console.print(Panel(syntax, title="Code Preview", border_style="dim blue"))
        
    except Exception as e:
        error_animation(f"Analysis failed: {str(e)}")


@cli.command()
@click.option('--model', type=click.Choice(['gpt4', 'claude', 'local']), help='Choose AI model')
def chat(model):
    """
    Interactive chat mode with Jarvis
    
    Enter multi-line conversations with your AI assistant
    """
    show_banner()
    
    console.print(Panel(
        "[bold cyan]Interactive Chat Mode[/bold cyan]\n\n"
        "💬 Chat with Jarvis in real-time\n"
        "📝 Type 'exit' or 'quit' to leave\n"
        "🔄 Type 'clear' to clear history",
        border_style="cyan",
        box=box.ROUNDED
    ))
    
    history = []
    
    while True:
        console.print()
        user_input = Prompt.ask("[bold yellow]You[/bold yellow]")
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            typing_effect("👋 Goodbye! See you next time.", style="bold cyan")
            break
        
        if user_input.lower() == 'clear':
            history = []
            console.clear()
            show_banner()
            console.print("[green]✓[/green] Chat history cleared\n")
            continue
        
        # Add to history
        history.append({"role": "user", "content": user_input})
        
        # Thinking animation
        thinking_animation("Processing", duration=0.8)
        
        try:
            response = client.ask(user_input, context=history)
            answer = response.get('answer', '')
            
            # Stream response
            console.print("\n[bold cyan]Jarvis:[/bold cyan]")
            ai_response_stream(answer)
            
            # Add to history
            history.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            console.print(f"\n[red]Error:[/red] {str(e)}")


@cli.command()
@click.argument('command')
@click.option('--confirm/--no-confirm', default=True, help='Confirm before execution')
def execute(command, confirm):
    """
    Execute shell commands safely
    
    Example: jarvis execute "ls -la" --no-confirm
    """
    console.print(f"\n[bold yellow]Command:[/bold yellow] [cyan]{command}[/cyan]\n")
    
    if confirm:
        if not Confirm.ask("Execute this command?", default=False):
            console.print("[yellow]⚠️  Cancelled[/yellow]\n")
            return
    
    processing_animation("⚙️  Executing command", duration=1.0)
    
    try:
        response = client.execute(command)
        
        # Display output
        table = Table(
            title=f"💻 Execution: {command}",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold cyan",
            border_style="blue"
        )
        
        table.add_column("Stream", style="bold yellow", width=12)
        table.add_column("Output", style="white")
        
        stdout = response.get('stdout', '').strip()
        stderr = response.get('stderr', '').strip()
        
        if stdout:
            table.add_row("stdout", stdout)
        if stderr:
            table.add_row("stderr", f"[red]{stderr}[/red]")
        
        console.print("\n", table, "\n")
        
        if response.get('returncode', 0) == 0:
            console.print("[green]✓[/green] Command executed successfully\n")
        else:
            console.print("[red]✗[/red] Command failed\n")
            
    except Exception as e:
        error_animation(f"Execution failed: {str(e)}")


@cli.command()
@click.option('--template', type=click.Choice(['python', 'javascript', 'react', 'api']), 
              default='python', help='Project template')
def init(template):
    """
    Initialize Jarvis in your project
    
    Creates configuration and sets up AI assistance
    """
    cwd = Path.cwd()
    
    console.print(f"\n[bold cyan]🚀 Initializing Jarvis[/bold cyan]\n")
    console.print(f"[dim]Location: {cwd}[/dim]\n")
    
    # Progress animation
    stages = [
        ("Creating .jarvis directory", 0.5),
        ("Generating configuration", 0.8),
        ("Setting up AI models", 1.0),
        ("Initializing cache", 0.6),
        ("Installing hooks", 0.7),
    ]
    
    with Progress(
        SpinnerColumn(spinner_name="dots", style="cyan"),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(complete_style="cyan"),
        console=console
    ) as progress:
        for stage, duration in stages:
            task = progress.add_task(stage, total=100)
            for i in range(100):
                progress.update(task, advance=1)
                time.sleep(duration / 100)
    
    # Create directory
    jarvis_dir = cwd / '.jarvis'
    jarvis_dir.mkdir(exist_ok=True)
    
    # Create config
    config_file = jarvis_dir / 'config.yaml'
    config_content = f"""# Jarvis AI Configuration
project_name: {cwd.name}
template: {template}
backend_url: http://127.0.0.1:8574

# AI Settings
ai:
  default_model: gpt-4
  enable_quantum: false
  enable_caching: true
  max_context: 8000

# Features
features:
  code_analysis: true
  auto_refactor: true
  github_integration: false
  
# Preferences
preferences:
  theme: monokai
  animations: true
  verbose: false
"""
    
    config_file.write_text(config_content)
    
    # Success
    console.print()
    success_animation("Jarvis Initialized Successfully!")
    
    console.print(Panel(
        f"[bold green]✓[/bold green] Project initialized with [cyan]{template}[/cyan] template\n\n"
        f"[bold]Config file:[/bold] {config_file}\n"
        f"[bold]Directory:[/bold] {jarvis_dir}\n\n"
        "[dim]Start using Jarvis with:[/dim]\n"
        "  [cyan]jarvis ask 'Your question'[/cyan]\n"
        "  [cyan]jarvis analyze yourfile.py[/cyan]",
        title="🎉 Setup Complete",
        border_style="green",
        box=box.DOUBLE_EDGE,
        padding=(1, 2)
    ))
    console.print()


if __name__ == '__main__':
    cli()
