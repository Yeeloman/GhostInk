# ghostink/cli.py
import typer
from typing_extensions import Annotated
from .core import GhostInk
from rich import print, pretty

pretty.install()
app = typer.Typer()

@app.command()
def main(message: Annotated[str, typer.Argument(...)]):
    print(f'first enter {message}')


if __name__ == "__main__":
    app()