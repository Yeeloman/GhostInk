# ghostink/cli.py
import typer
from typing import Optional
from rich import print, pretty
from rich.console import Console
from typing_extensions import Annotated
# from .core import GhostInk

__version__ = "0.1.0"

pretty.install()
console = Console()
app = typer.Typer(no_args_is_help=True, help="this is help message")


@app.callback(invoke_without_command=True)
def main(
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
    ] = None
):
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
