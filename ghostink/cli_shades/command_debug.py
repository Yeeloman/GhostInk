import typer
from typing_extensions import Annotated
from rich import pretty
from rich.console import Console

pretty.install()
console = Console()


def debug_command(
    message: Annotated[str, typer.Argument(...)],
):
    """
    Prints a debug message to the console.
    """
    console.print(f"debug: {message}")
