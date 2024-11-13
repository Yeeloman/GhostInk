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

def create_new_todo(todo_id, todo_list_obj):
    new_todo = {}

    new_todo = {"id": todo_id}
    new_todo["title"] = Prompt.ask(
        "Title", default=f"Todo N°{todo_id}", show_default=True
    )
    new_todo["description"] = Prompt.ask("Description", default="", show_default=False)
    new_todo["priority"] = Prompt.ask(
        "Priority",
        choices=["Low", "Medium", "High"],
        case_sensitive=False,
        show_choices=True,
        default="Medium",
    )
    new_todo["status"] = Prompt.ask(
        "Status",
        choices=["Pending", "Completed"],
        case_sensitive=False,
        show_choices=True,
        default="Pending",
    )
    tags = Prompt.ask("Tags (comma-separated)")
    new_todo["tags"] = [tag.strip() for tag in tags.split(",")]
    if new_todo["status"] == "Pending":
        new_todo["subtasks"] = []
        subtask_number = int(
            Prompt.ask("How many Subtasks", default="0", show_default=True)
        )
        for i in range(subtask_number):
            subtask = {
                "id": i + 1,
                "title": Prompt.ask(f"Title for subtask {i + 1}"),
                "status": "Pending",
            }

            new_todo["subtasks"].append(subtask)

    todo_list_obj["TODO"].append(new_todo)

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

    todo_list_obj = None
    todo_id = 1

    GHOST_PATH = ctx.obj.get("GHOST_PATH")
    file_path = Path(GHOST_PATH) / f"{filename}.yml"

    if file_path.exists():
        todo_list_obj = yaml.safe_load(file_path.open("r"))
        if todo_list_obj:
            todo_id = len(todo_list_obj["TODO"]) + 1
        else:
            todo_list_obj = {"TODO": []}
    else:
        todo_list_obj = {"TODO": []}
        file_path.touch()

    create_new_todo(todo_id, todo_list_obj)
    todo_yml = yaml.dump(todo_list_obj, sort_keys=False)
    file_path.write_text(todo_yml)
    console.print(f'Todo added to {file_path}')
