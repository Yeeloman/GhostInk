import os
import yaml
import json
import shutil
import random
import inspect
from enum import Enum
from rich import pretty
from rich.console import Console
from rich.text import Text
from rich.syntax import Syntax
from datetime import datetime
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
        - TODO: Represents a etch to be done.
        - DEBUG: Represents debug information.
        - INFO: Represents informational messages.
        - ERROR: Represents warning messages.
        """

        TODO = "TODO"
        INFO = "INFO"
        DEBUG = "DEBUG"
        WARN = "WARN"
        ERROR = "ERROR"
        _ECHO = "ECHO"  # only for internal use

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
        self.etches = set()
        self.project_root = project_root

        # alias the inkdrop/haunt method with just drop/ln
        self.drop = self.inkdrop
        self.ln = self.haunt

        self._create_etch_dir()

    def clean(self):
        ghost_path = os.path.join(self.project_root, ".ghost")
        if os.path.exists(ghost_path):
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
        etch_input: Union[str, None] = None,
        shade: Optional["GhostInk.shade"] = None,
        echoes: Optional[List[str]] = None,
        filename: Optional[str] = None,
    ) -> None:
        if filename:
            # ? treating the file should be in this lvl
            # ? in case there are multiple shades
            filename_with_ext = f"{filename}.yml"
            file_path = os.path.join(self.project_root, ".ghost", filename_with_ext)
            try:
                with open(file_path, "r") as file:
                    etch_from_file = yaml.safe_load(file)
                    for shade_file, etch_file in etch_from_file.items():
                        shade_cls = ShadeRegistry.get_shade_class(
                            self.shade[shade_file]
                        )
                        shade_instance = shade_cls(ghost_ink=self)
                        shade_instance.dropper(etch_file)
            except FileNotFoundError:
                raise FileExistsError("The file do not exist")
        else:
            if shade is None:
                shade = self.shade.TODO
            shade_cls = ShadeRegistry.get_shade_class(shade)
            shade_instance = shade_cls(ghost_ink=self)
            shade_instance.inker(etch_input, shade, echoes)

    def whisper(
        self,
        shade_mask: str = None,
        file_mask: str = None,
        echo_mask: Optional[List[str]] = None,
    ) -> None:
        """
        Prints filtered and sorted etchs based on the provided shade_mask and file_mask.

        Parameters:
        - shade_mask (GhostInk.shade): The shade to filter etchs by (default: None).
        - file_mask (str): The filename to filter etchs by (default: None).
        """
        # Display Title
        console.print(f"""\n{self.title}""", style="bold bright_cyan")
        filtered_etches = self.etches.copy()  # Start with all etches

        # If no masks are provided, print all etches
        if shade_mask is None and file_mask is None and echo_mask is None:
            filtered_etches = sorted(filtered_etches, key=lambda x: x[0].value)
        else:
            # Apply filtering
            if shade_mask:
                filtered_etches = {
                    etch for etch in filtered_etches if etch[0] == shade_mask
                }

            # Filter by file
            if file_mask:
                filtered_etches = {
                    etch for etch in filtered_etches if etch[2] == file_mask
                }

            # Filter by echoes
            if echo_mask:
                shade_cls = ShadeRegistry.get_shade_class(self.shade.TODO)
                shade_instance = shade_cls(ghost_ink=self)
                formatted_echoes = shade_instance._format_echoes(echoes=echo_mask)
                filtered_etches = {
                    etch
                    for etch in filtered_etches
                    if any(echo in etch[5] for echo in formatted_echoes)
                }

        sorted_etches = sorted(filtered_etches, key=lambda x: x[0].value)

        # Print etchs
        for etch_shade, etch, file, line, func, echoes in sorted_etches:
            newline = Text("\n")
            newline.append(
                self._format_etch(etch_shade, etch, file, line, func, echoes)
            )
            console.print(newline)
        # Caller information
        caller_frame = inspect.stack()[1]
        caller_file = os.path.relpath(caller_frame.filename, start=self.project_root)
        caller_line = caller_frame.lineno

        text = Text("\nPrinted from: ")
        text.append(caller_file, style="red")
        text.append(" at line ", style="none")
        text.append(str(caller_line), style="bold yellow")
        console.print(text)

        console.print(
            f"Review completed etchs and remove them as necessary.\n",
            style="bright_red",
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
            self.shade._ECHO: f"{random.choice(foreground_colors)} on {random.choice(background_colors)}",
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
        caller_frame = inspect.stack()[3]
        full_path = caller_frame.filename
        relative_path = os.path.relpath(full_path, start=self.project_root)
        return relative_path, caller_frame.lineno, caller_frame.function

    def _format_etch_from_object(self, etch_input: any) -> str:
        """
        Convert a dictionary or object to a string
        representation suitable for a etch.

        Parameters:
        - etch_input (dict or object): The input to format.

        Returns:
        - str: A formatted string representing the etch.
        """
        if isinstance(etch_input, (dict, list, tuple)):
            return json.dumps(etch_input, indent=4)
        elif isinstance(etch_input, set):
            return json.dumps(list(etch_input), indent=4)
        elif isinstance(etch_input, str):
            return etch_input
        elif hasattr(etch_input, "__dict__"):
            return json.dumps(etch_input.__dict__, indent=4)
        else:
            etch_str = str(etch_input)
            return f"{etch_str}"

    def _format_etch(self, etch_shade, etch, file, line, func, echoes):
        """
        Formats a task for printing.

        Parameters:
        - etch (tuple): The task tuple to format.

        Returns:
        - str: The formatted string.
        """
        filename = file.split("/")[-1]
        path = "/".join(file.split("/")[:-1])
        colored_filename = self._color_text(etch_shade, filename)
        colored_shade = self._color_text(etch_shade)
        if echoes:
            colored_echoes = Text("")
            for echo in echoes:
                colored_echoes.append(" ")
                colored_echoes.append(
                    self._color_text(self.shade._ECHO, " " + echo + " ")
                )
            colored_echoes.append("\n")

        else:
            colored_echoes = Text("")
        colored_line_nb = self._color_text(etch_shade, str(line))
        output = Text(f"[")
        output.append(colored_shade)
        output.append(f"] {etch}\n")
        output.append(colored_echoes)
        output.append(f"(Ln:")
        output.append(colored_line_nb)
        output.append(f" - {func} in {path}")
        output.append(colored_filename)
        return output

    def _create_etch_dir(self):
        # sets up the dir where the logs and etches live
        ghost_dir_path = os.path.join(self.project_root, ".ghost")
        os.makedirs(ghost_dir_path, exist_ok=True)

        example_path = os.path.join(ghost_dir_path, "example.yml")
        content = {
            "TODO": [
                {
                    "title": "Title of the main task",
                    "description": "Detailed description of the task",
                    "priority": "High",  # Low, Medium
                    "subtasks": [
                        {"name": "Subtask 1", "status": "Pending"},  # completed
                        {"name": "Subtask 2", "status": "In-progress"},
                        {"name": "Subtask 2", "status": "Completed"},
                    ],
                }
            ]
        }
        with open(example_path, "w") as file:
            yaml.dump(content, file)


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
        if shade == GhostInk.shade._ECHO:
            raise ValueError(
                "Attempted to use shade '_ECHO', which is not allowed for etch addition."
            )
        elif shade not in GhostInk.shade:
            raise ValueError("unvalid shade")
        return cls.shade_classes.get(shade)


__all__ = ["GhostInk"]
