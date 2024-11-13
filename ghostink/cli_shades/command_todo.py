import os
import yaml
import typer
from rich import pretty
from pathlib import Path
from rich.prompt import Prompt
from rich.console import Console
from typing_extensions import Annotated

pretty.install()
console = Console()

GHOST_PATH = None


def todo(
    ctx: typer.Context,
    filename: Annotated[
        str,
        typer.Option(
            "--filename",
            "-f",
            show_default=None,
            help="The name of the file to process.",
        ),
    ],
):
    global GHOST_PATH
    todo_obj = {}
    GHOST_PATH = ctx.obj.get("GHOST_PATH")


    filename_yml = f'{filename}.yml'
    file_path = os.path.join(GHOST_PATH, filename_yml)
    
    todo_obj['title'] = Prompt.ask('What is the title')
    # with open(file_path, 'a+') as f:
    #     pass

