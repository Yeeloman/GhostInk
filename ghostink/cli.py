# ghostink/cli.py
import os
import typer
from pathlib import Path
from typing import Optional
from rich import print, pretty
from rich.console import Console
from typing_extensions import Annotated

# from .core import GhostInk

__version__ = "0.1.0"

pretty.install()
console = Console()
app = typer.Typer(no_args_is_help=True, help="this is help message")

CONFIG_FILE = Path.home() / ".ghostink_config"
def load_project_path() -> Optional[Path]:
    """Load project path from GHOSTINK env variable or config file."""
    if os.getenv("GHOSTINK"):
        return Path(os.getenv("GHOSTINK"))
    elif CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as file:
            line = file.read().strip()
            if line.startswith("GHOSTINK="):
                path = line.split("=", 1)[1].strip().strip('"').strip("'")
                return Path(path)
    return None

def save_project_path(path: Path):
    """Save the project path to the config file."""
    with open(CONFIG_FILE, "w") as file:
        file.write(str(f"GHOSTINK='{path}'"))

# Initialize project path from the environment or config
PROJECT_PATH = load_project_path()

@app.callback(invoke_without_command=True)
def main(
    set_path: Annotated[
            Optional[Path], typer.Option(help="Set the project path." "--set-path")
    ] = PROJECT_PATH,
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            callback=lambda v: (
                console.print(
                    f"[bold bright_magenta]Ghosty[/bold bright_magenta]: {__version__}"
                )
                if v
                else None
            ),
            is_eager=True,
            help="Show the Ghosty version and exit.",
        ),
    ] = None,
):
    global PROJECT_PATH
    if set_path:
        PROJECT_PATH = set_path.expanduser().resolve()
        save_project_path(PROJECT_PATH)

    if not PROJECT_PATH:
        console.print(
            "[bold red]Error:[/bold red] GHOSTINK environment variable not set and no path provided with --set-path.\n"
            "Please set the path using one of the following methods:\n"
            "1. Export the GHOSTINK variable: [bold]export GHOSTINK=\"~/path/to/project_root\"[/bold]\n"
            "2. Use the [bold]--set-path[/bold] option to set it for this session: [bold]ghosty --set-path ~/path/to/project_root[/bold]"
            "\n[blue]Note[/blue]: The first method (GHOSTINK environment variable) has higher priority than the --set-path option."
        )
        raise typer.Exit(code=1)
    if version:
        raise typer.Exit()


@app.command()
def todo(
    message: Annotated[str, typer.Argument(...)],
):
    console.print(f"todo: {message}")


@app.command()
def info(
    message: Annotated[str, typer.Argument(...)],
):
    """
    Prints an informational message to the console.
    """
    console.print(f"info: {message}")


@app.command()
def debug(
    message: Annotated[str, typer.Argument(...)],
):
    console.print(f"debug: {message}")


@app.command()
def warn(
    message: Annotated[str, typer.Argument(...)],
):
    console.print(f"warn: {message}")


@app.command()
def error(
    message: Annotated[str, typer.Argument(...)],
):
    console.print(f"error: {message}")


if __name__ == "__main__":
    app()
