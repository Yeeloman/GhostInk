import os
import yaml
import json
import shutil
import random
import inspect
from enum import Enum
from rich import pretty
from pathlib import Path
from rich.text import Text
from datetime import datetime
from rich.console import Console
from typing import List, Optional, Union
from .shades import Todo, Info, Debug, Warn, Error

pretty.install()
console = Console()


class GhostInk:
    """
    Prints file name, line number, function name, and timestamp of the method call.
    """

    class shade(Enum):
        """
        Defines an Enum class 'shade' with options:
        - TODO: Represents a entry to be done.
        - DEBUG: Represents debug information.
        - INFO: Represents informational messages.
        - ERROR: Represents warning messages.
        """

        TODO = "TODO"
        INFO = "INFO"
        DEBUG = "DEBUG"
        WARN = "WARN"
        ERROR = "ERROR"
        _tag = "tag"  # only for internal use

    def get_shades(self):
        return self.shade

    def __init__(
        self,
        title: str = "GhostInk",
        project_root: str = ".",
    ):
        """
        Initializes a GhostInk instance with optional logging to a file.

        Parameters:
        - title (str): The title of the instance (default: "GhostInk").
        - project_root (str): The root directory of the project (default: ".").

        Sets up a logger if logging to a file is enabled.
        """
        self.title = title
        self.entries = set()
        self.project_root = os.getenv("GHOSTINK") or project_root
        self.Group = Path(self.project_root) / ".ghost" / self.title

        # alias the inkdrop/haunt method with just drop/ln
        self.drop = self.inkdrop
        self.ln = self.haunt

        self._create_entry_dir()

    def clean(self):
        ghost_path = Path(self.project_root) / ".ghost"
        if ghost_path.exists():
            shutil.rmtree(ghost_path)

    def haunt(self, message: str = None) -> None:
        """
        Prints the file name, line number, function name, and timestamp of where this method is called.

        Parameters:
        - message (str): Optional message to print before the file information.

        Prints the file information along with the message if provided, including the file name, line number, function name, and timestamp.
        """
        # Get the calling frame information
        caller_frame = inspect.stack()[1]
        caller_file = os.path.basename(caller_frame.filename)  # File name
        caller_line = caller_frame.lineno  # Line number
        caller_func = caller_frame.function  # Function name

        # Get the current timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")  # Time down to milliseconds

        output_text = Text()
        if message:
            console.print(message)
            output_text.append(f"└── {caller_file}", style="bold yellow")
        else:
            output_text.append(f"{caller_file}", style="bold yellow")

        output_text.append(":", style="dim")
        output_text.append(f"{caller_line}", style="bold magenta")
        output_text.append(f" in {caller_func}()", style="bold red")
        output_text.append(f" at {timestamp}", style="dim")

        console.print(output_text)

    def inkdrop(
        self,
        entry_input: Union[str, None] = "Note: This is only the default message.",
        shade: Optional["GhostInk.shade"] = None,
        tags: Optional[List[str]] = None,
        filename: Optional[str] = None,
    ) -> None:
        if filename:
            file_path = self.Group / f"{filename}.yml"
            try:
                with file_path.open("r") as file:
                    entries_from_file = yaml.safe_load(file)
                    for shade_from_file, entry_from_file in entries_from_file.items():
                        shade_cls = ShadeRegistry.get_shade_class(
                            self.shade[shade_from_file]
                        )
                        shade_instance = shade_cls(ghost_ink=self)
                        shade_instance.dropper(entry_from_file)
            except FileNotFoundError:
                raise FileExistsError("The specified file do not exist")
        else:
            if shade is None:
                shade = self.shade.TODO
            shade_cls = ShadeRegistry.get_shade_class(shade)
            shade_instance = shade_cls(ghost_ink=self)
            shade_instance.inker(entry_input, shade, tags)

    def whisper(
        self,
        filter_shade: str = None,
        filter_file: str = None,
        filter_tag: Optional[List[str]] | str = None,
    ) -> None:
        """
        Prints filtered and sorted entries based on the provided filter_shade and filter_file.

        Parameters:
        - filter_shade (GhostInk.shade): The shade to filter entries by (default: None).
        - filter_file (str): The filename to filter entries by (default: None).
        """
        # change the tag to a list for process
        if isinstance(filter_tag, str):
            filter_tag = [filter_tag]

        # Display Title
        console.rule(f"""{self.title}""", style="bold bright_cyan")
        filtered_entries = self.entries.copy()  # Start with all entries

        # If no masks are provided, print all entries
        if filter_shade is None and filter_file is None and filter_tag is None:
            filtered_entries = sorted(filtered_entries, key=lambda x: x[0].value)
        else:
            # Apply filtering
            if filter_shade:
                filtered_entries = {
                    entry for entry in filtered_entries if entry[0] == filter_shade
                }

            # Filter by file
            if filter_file:
                filtered_entries = {
                    entry for entry in filtered_entries if entry[2] == filter_file
                }

            # Filter by tags
            if filter_tag:
                shade_cls = ShadeRegistry.get_shade_class(self.shade.TODO)
                shade_instance = shade_cls(ghost_ink=self)
                formatted_tags = shade_instance._format_tags(tags=filter_tag)
                filtered_entries = {
                    entry
                    for entry in filtered_entries
                    if any(tag in entry[5] for tag in formatted_tags)
                }

        sorted_entries = sorted(filtered_entries, key=lambda x: x[0].value)

        # Print entries
        for entry_shade, entry, file, line, func, tags in sorted_entries:
            newline = Text("\n")
            newline.append(
                self._format_entry(entry_shade, entry, file, line, func, tags)
            )
            console.print(newline)

        self.footer()

    def footer(self):
        # Caller information
        caller_frame = inspect.stack()[1]
        caller_file = os.path.relpath(caller_frame.filename, start=self.project_root)
        caller_line = caller_frame.lineno

        text = Text("\nPrinted from: ")
        text.append(caller_file, style="red")
        text.append(" at line ", style="none")
        text.append(str(caller_line), style="bold yellow")
        console.print(text, justify="center")

        console.rule(
            f"[bold bright_red]Review completed entries and remove them as necessary.[/bold bright_red]",
        )

    def _color_text(self, shade: shade, text: str = "") -> None:
        """
        Color the text based on the debug shade using colorama.

        Parameters:
        - text (str): The text to color.
        - shade (self.shade): The shade that determines the color.

        Returns:
        - str: Colored text.
        """
        foreground_colors = [
            "black",
            "red",
            "green",
            "yellow",
            "blue",
            "magenta",
            "cyan",
            "white",
            "bright_black",
            "bright_red",
            "bright_green",
            "bright_yellow",
            "bright_blue",
            "bright_magenta",
            "bright_cyan",
            "bright_white",
        ]

        # List of basic and bright background colors
        background_colors = [
            "black",
            "red",
            "green",
            "yellow",
            "blue",
            "magenta",
            "cyan",
            "white",
            "bright_black",
            "bright_red",
            "bright_green",
            "bright_yellow",
            "bright_blue",
            "bright_magenta",
            "bright_cyan",
            "bright_white",
        ]

        # Define color mapping for each shade
        colors = {
            self.shade.TODO: "yellow",
            self.shade.DEBUG: "blue",
            self.shade.INFO: "magenta",
            self.shade.WARN: "red",
            self.shade.ERROR: "bold red",
            # todo shuffle again if fr and bg are the same
            self.shade._tag: f"{random.choice(foreground_colors)} on {random.choice(background_colors)}",
        }

        # Choose the style for the shade
        style = colors.get(shade)
        # Create and return the `Text` object with the applied style
        content = shade.name if text == "" else text
        return Text(content, style=style)

    def _get_relative_path(self) -> tuple[str, int, str]:
        """
        Return the relative path and line number of the code file
        calling this method, relative to the project's base directory.
        """
        # TODO change from os.path to Path later
        caller_frame = inspect.stack()[3]
        full_path = caller_frame.filename
        relative_path = os.path.relpath(full_path, start=self.project_root)
        return relative_path, caller_frame.lineno, caller_frame.function

    def _format_entry_from_object(self, entry_input: any) -> str:
        """
        Convert a dictionary or object to a string
        representation suitable for a entry.

        Parameters:
        - entry_input (dict or object): The input to format.

        Returns:
        - str: A formatted string representing the entry.
        """
        if isinstance(entry_input, (dict, list, tuple)):
            return json.dumps(entry_input, indent=4)
        elif isinstance(entry_input, set):
            return json.dumps(list(entry_input), indent=4)
        elif isinstance(entry_input, str):
            return entry_input
        elif hasattr(entry_input, "__dict__"):
            return json.dumps(entry_input.__dict__, indent=4)
        else:
            entry_str = str(entry_input)
            return f"{entry_str}"

    def _format_entry(self, entry_shade, entry, file, line, func, tags):
        """
        Formats a task for printing.

        Parameters:
        - entry (tuple): The task tuple to format.

        Returns:
        - str: The formatted string.
        """
        filename = file.split("/")[-1]
        path = "/".join(file.split("/")[:-1])
        colored_filename = self._color_text(entry_shade, filename)
        colored_shade = self._color_text(entry_shade)
        if tags:
            colored_tags = Text("")
            for tag in tags:
                colored_tags.append(" ")
                colored_tags.append(self._color_text(self.shade._tag, " " + tag + " "))
            colored_tags.append("\n")

        else:
            colored_tags = Text("")
        colored_line_nb = self._color_text(entry_shade, str(line))
        output = Text(f"[")
        output.append(colored_shade)
        output.append(f"] {entry}\n")
        output.append(colored_tags)
        output.append(f"(Ln:")
        output.append(colored_line_nb)
        output.append(f" - {func} in {path}")
        output.append(colored_filename)
        return output

    def _create_entry_dir(self):
        # sets up the dir where the logs and entries live
        ghost_dir_path = self.Group
        ghost_dir_path.mkdir(parents=True, exist_ok=True)

        example_path = ghost_dir_path / "example.yml"
        content = {
            "TODO": [
                {
                    "id": 1,
                    "title": "Title of the main task",
                    "description": "Detailed description of the task",
                    "priority": "High",  # Low, Medium
                    "status": "Pending",
                    "tags": ["tag1", "tag2"],
                    "subtasks": [
                        {"title": "Subtask 1", "status": "Pending"},  # completed
                        {"title": "Subtask 2", "status": "Completed"},
                    ],
                },
                {
                    "id": 2,
                    "title": "Title of the secondary task",
                    "description": "Detailed description of the task",
                    "priority": "Medium",  # Low, Medium
                    "status": "Completed",
                    "tags": "another tag",
                },
                {
                    "id": 3,
                    "title": "Title of the third task",
                    "description": "Detailed description of the task",
                    "priority": "Low",  # Low, Medium
                    "status": "Pending",
                    "subtasks": [
                        {"title": "Subtask 9651", "status": "Pending"},  # completed
                        {"title": "Subtask 102", "status": "Completed"},
                    ],
                },
            ],
            # "ERROR": [
            #     {
            #         "id": 1,
            #         "title": "this is error task",
            #         "description": "the detailed desc",
            #     }
            # ],
        }
        with example_path.open("w") as file:
            yaml.dump(content, file, sort_keys=False)

    def __str__(self):
        return f"{self.title}: {len(self.entries)} entries"


class ShadeRegistry:
    # Dictionary mapping each shade Enum to its corresponding class
    shade_classes = {
        GhostInk.shade.TODO: Todo,
        GhostInk.shade.INFO: Info,
        GhostInk.shade.DEBUG: Debug,
        GhostInk.shade.WARN: Warn,
        GhostInk.shade.ERROR: Error,
    }

    @classmethod
    def get_shade_class(cls, shade: GhostInk.shade):
        """Returns the corresponding class for a given shade Enum."""
        if shade == GhostInk.shade._tag:
            raise ValueError(
                "Attempted to use shade '_tag', which is not allowed for entry addition."
            )
        elif shade not in GhostInk.shade:
            raise ValueError("unvalid shade")
        return cls.shade_classes.get(shade)


__all__ = ["GhostInk"]
