import typer
from typing_extensions import Annotated
from rich import pretty
from rich.console import Console

pretty.install()
console = Console()


def warn_command(
    message: Annotated[str, typer.Argument(...)],
):
    """
    Prints a warn message to the console.
    """
    console.print(f"warn: {message}")
