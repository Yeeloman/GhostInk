import typer
from typing_extensions import Annotated
from rich import pretty
from rich.console import Console

pretty.install()
console = Console()
app = typer.Typer(no_args_is_help=True, help="Help message for todo subcommand")

def warn_command(
    message: Annotated[str, typer.Argument(...)],
):
    """
    Prints a warn message to the console.
    """
    console.print(f"warn: {message}")


if __name__=="__main__":
    app()