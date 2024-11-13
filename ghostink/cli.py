# ghostink/cli.py
import os
import typer
from rich import pretty
from pathlib import Path
from typing import Optional
from rich.console import Console
from typing_extensions import Annotated
from .cli_shades import (
    command_todo,
    command_info,
    command_debug,
    command_warn,
    command_error,
)

# from .core import GhostInk

__version__ = "0.1.0"

pretty.install()
console = Console()
app = typer.Typer(
    no_args_is_help=True,
    help="To use ghosty you must set up the GHOSTINK (project root path).",
)

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
GHOST_PATH = None
PROJECT_PATH = load_project_path()


@app.callback(invoke_without_command=True)
def ghosty(
    ctx: typer.Context,
    project_root: Annotated[
        Optional[Path],
        typer.Option(
            "--project-root",
            "-p",
            exists=True,
            dir_okay=True,
            file_okay=False,
            help="Set the project path.",
        ),
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
            help="Show the Ghosty version.",
        ),
    ] = None,
):
    global PROJECT_PATH
    global GHOST_PATH
    if project_root:
        PROJECT_PATH = project_root.expanduser().resolve()
        save_project_path(PROJECT_PATH)
        GHOST_PATH = os.path.join(PROJECT_PATH, ".ghost")

    if not PROJECT_PATH:
        console.print(
            "[bold red]Error:[/bold red] GHOSTINK environment variable not set and no path provided with --set-path.\n"
            "Please set the path using one of the following methods:\n"
            '1. Export the GHOSTINK variable: [bold]export GHOSTINK="~/path/to/project_root"[/bold]\n'
            "2. Use the [bold]--set-path[/bold] option to set it for this session: [bold]ghosty --set-path ~/path/to/project_root[/bold]"
            "\n[blue]Note[/blue]: The first method (GHOSTINK environment variable) has higher priority than the --set-path option."
        )
        raise typer.Exit(code=1)
    if version:
        raise typer.Exit()
    
    ctx.obj = {"GHOST_PATH": GHOST_PATH}
    Path(GHOST_PATH).mkdir(exist_ok=True)


# adding the subcommands
app.command("todo", help="Everything related to Todo shade in ghostink")(
    command_todo.todo
)
app.command("t", help="Alias of todo")(command_todo.todo)
app.command("info", help="Everything related to Info shade in ghostink")(
    command_info.info_command
)
app.command("debug", help="Everything related to Debug shade in ghostink")(
    command_debug.debug_command
)
app.command("warn", help="Everything related to Warn shade in ghostink")(
    command_warn.warn_command
)
app.command("error", help="Everything related to Error shade in ghostink")(
    command_error.error_command
)

if __name__ == "__main__":
    app()
