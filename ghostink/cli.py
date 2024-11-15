# ghostink/cli.py
import os
import typer
from rich import pretty
from pathlib import Path
from rich.text import Text
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
APP_NAME = "ghosty"

pretty.install()
console = Console()
app = typer.Typer(
    no_args_is_help=True,
    help="To use ghosty you must set up the GHOSTINK (project root path).",
)

APP_DIR = Path(typer.get_app_dir(APP_NAME))
APP_DIR.mkdir(exist_ok=True)
CONFIG_FILE = APP_DIR / ".ghostink_config"


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
    show_path: Annotated[
        Optional[bool],
        typer.Option(
            "--show-path",
            "-P",
            help="Show the .ghost directory path.",
        ),
    ] = None,
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
    group: Annotated[
        Optional[str],
        typer.Option(
            "--grp",
            "-g",
            help="Specify the title for the GhostInk CLS instance to sync with.",
        ),
    ] = "GhostInk",
    list_files: Annotated[
        Optional[bool],
        typer.Option(
            "--list", "-l", show_default=False, help="List all the files in a group."
        ),
    ] = False,
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
        GHOST_PATH = Path(PROJECT_PATH) / ".ghost" / group

    if not PROJECT_PATH:
        console.print(
            "[bold red]Error:[/bold red] GHOSTINK environment variable not set and no path provided with --set-path.\n"
            "Please set the path using one of the following methods:\n"
            '1. Export the GHOSTINK variable: [bold]export GHOSTINK="~/path/to/project_root"[/bold]\n'
            "2. Use the [bold]--set-path[/bold] option to set it for this session: [bold]ghosty --set-path ~/path/to/project_root[/bold]"
            "\n[blue]Note[/blue]: The first method (GHOSTINK environment variable) has higher priority than the --set-path option.",
            soft_wrap=True,
        )
        raise typer.Exit(code=1)
    if version:
        raise typer.Exit()
    if list_files:
        files = [f for f in GHOST_PATH.glob("*")]
        file_list = Text("")
        out_str = " ".join(f.name for f in files)
        file_list.append(out_str)
        if not file_list:
            console.print("No files under the current Group", style="bold bright_red")
        else:
            console.print(file_list)
        raise typer.Exit()
    if show_path:
        console.print(f".ghost dir in: {GHOST_PATH}")
        raise typer.Exit()
    ctx.obj = {"GHOST_PATH": GHOST_PATH}
    GHOST_PATH.mkdir(parents=True, exist_ok=True)


# adding the subcommands
app.command("todo")(command_todo.todo)
app.command("t", hidden=True)(command_todo.todo)
# app.command("info")(command_info.info_command)
# app.command("debug")(command_debug.debug_command)
# app.command("warn")(command_warn.warn_command)
# app.command("error")(command_error.error_command)

if __name__ == "__main__":
    app()
