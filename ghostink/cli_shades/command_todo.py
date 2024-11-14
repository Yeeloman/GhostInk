import yaml
import typer
from rich import pretty
from pathlib import Path
from typing import Optional
from rich.prompt import Prompt, Confirm
from rich.console import Console
from typing_extensions import Annotated

pretty.install()
console = Console()

FILE_PATH = None


def create_todo_entry() -> None:
    todo_list_obj = None
    new_todo = {}
    todo_id = 1
    console.rule("[bold red]TODO[/bold red]")
    if FILE_PATH.exists():
        todo_list_obj = yaml.safe_load(FILE_PATH.open("r"))
        if todo_list_obj and "TODO" in todo_list_obj:
            todo_id = len(todo_list_obj["TODO"]) + 1
        else:
            todo_list_obj = {"TODO": []}
    else:
        todo_list_obj = {"TODO": []}
        FILE_PATH.touch()

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
    todo_yml = yaml.dump(todo_list_obj, sort_keys=False)
    FILE_PATH.write_text(todo_yml)
    console.print(f"Todo added to {FILE_PATH}")


def delete_todo_entry(todo_id: int) -> None:
    if not FILE_PATH.exists():
        console.print("The specified file does not exist.")
        return

    todo_list_obj = yaml.safe_load(FILE_PATH.open("r"))
    if todo_list_obj and "TODO" in todo_list_obj:
        original_count = len(todo_list_obj["TODO"])
        todo_list_obj["TODO"] = [
            todo for todo in todo_list_obj["TODO"] if todo["id"] != todo_id
        ]
        new_count = len(todo_list_obj["TODO"])

        if new_count < original_count:
            todo_yml = yaml.dump(todo_list_obj, sort_keys=False)
            FILE_PATH.write_text(todo_yml)
        else:
            console.print(f"No Todo found with the ID {todo_id}")
    else:
        console.print("No TODOs found in the file.")


def delete__all_todo_entries() -> None:
    if not FILE_PATH.exists():
        console.print("The specified file does not exist.")
        return

    confirm_delete = Confirm.ask(
        "Are you sure you want to delete all TODO entries?", default=False
    )
    if not confirm_delete:
        console.print("Deletion canceled.")
        return


    with console.status('deleting all entries...', spinner="dots2"):
        todo_list_obj = yaml.safe_load(FILE_PATH.open("r"))
        if todo_list_obj and "TODO" in todo_list_obj:
            todo_list_obj.pop("TODO")
            todo_yml = yaml.dump(todo_list_obj, sort_keys=False)
            FILE_PATH.write_text(todo_yml)
        else:
            console.print("No TODOs found in the file.")


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
    new_entry: Annotated[
        Optional[bool],
        typer.Option(
            "--new",
            "-n",
            help="create a new todo entry in the specified file",
        ),
    ] = True,
    delete: Annotated[
        Optional[int],
        typer.Option(
            "--delete",
            "-d",
            show_default=False,
            help="delete a todo entry in the specified file",
        ),
    ] = -1,
    delete_all: Annotated[
        Optional[bool],
        typer.Option(
            "--delete-all",
            "-D",
            show_default=False,
            help="delete all todo entries in the specified file",
        ),
    ] = False,
):
    """
    Manage to-do entries within a YAML file.(Alias: "t")
    """
    global FILE_PATH

    ghost_path = ctx.obj.get("GHOST_PATH")
    FILE_PATH = Path(ghost_path) / f"{filename}.yml"

    if delete >= 0:
        delete_todo_entry(delete)
    elif delete_all:
        delete__all_todo_entries()
    elif new_entry:
        create_todo_entry()