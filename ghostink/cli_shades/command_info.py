import typer
from typing_extensions import Annotated
from rich import pretty
from rich.console import Console

pretty.install()
console = Console()

def info_command(
    message: Annotated[str, typer.Argument(...)],
):
    """
    Prints an informational message to the console.
    """
    console.print(f"info: {message}")