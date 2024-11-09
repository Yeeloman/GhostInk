import os
import yaml
import json
import shutil
import random
import inspect
import logging
import traceback
from enum import Enum
from datetime import datetime
from typing import List, Optional, Union
from colorama import Fore, Back, Style, init
from .shades import Todo, Info, Debug, Warn, Error

# Initialize colorama
init(autoreset=True)


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
        log_to_file: bool = False,
        log_file: str = "ghostink.log",
    ):
        """
        Initializes a GhostInk instance with optional logging to a file.

        Parameters:
        - title (str): The title of the instance (default: "GhostInk").
        - project_root (str): The root directory of the project (default: ".").
        - log_to_file (bool): Whether to log messages to a file (default: False).
        - log_file (str): The name of the log file (default: "ghostink.log").

        Sets up a logger if logging to a file is enabled.
        """
        self.title = title
        self.etches = set()
        self.project_root = project_root
        self.log_to_file = log_to_file
        self.log_file = log_file
        self.logger = None

        # alias the inkdrop/haunt method with just drop/ln
        self.drop = self.inkdrop
        self.ln = self.haunt

        # sets up the dir where the logs and etches live
        ghost_dir = os.path.join(self.project_root, ".ghost")
        os.makedirs(ghost_dir, exist_ok=True)

        if log_to_file:
            self._setup_logger(log_file)

    def clean(self):
        ghost_path = os.path.join(self.project_root, ".ghost")
        if os.path.exists(ghost_path):
            shutil.rmtree(ghost_path)

    def haunt(self, curse: str = None) -> None:
        """
        Prints the file name, line number, function name, and timestamp of where this method is called.

        Parameters:
        - curse (str): Optional message to print before the file information.

        Prints the file information along with the message if provided, including the file name, line number, function name, and timestamp.
        """
        # Get the calling frame information
        caller_frame = inspect.stack()[1]
        caller_file = os.path.basename(caller_frame.filename)  # File name
        caller_line = caller_frame.lineno  # Line number
        caller_func = caller_frame.function  # Function name

        # Get the current timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")  # Time down to milliseconds

        if curse:
            print(curse)
            print(
                f"""{Style.BRIGHT}{Fore.YELLOW}└── {
                    caller_file}{Style.RESET_ALL}:"""
                f"""{Style.BRIGHT}{Fore.MAGENTA}{
                    caller_line}{Style.RESET_ALL} in """
                f"""{Style.BRIGHT}{Fore.RED}{caller_func}(){Style.RESET_ALL} at {
                    timestamp}"""
            )
        else:
            print(
                f"""{Style.BRIGHT}{Fore.YELLOW}{caller_file}{Style.RESET_ALL}:"""
                f"""{Style.BRIGHT}{Fore.MAGENTA}{
                    caller_line}{Style.RESET_ALL} in """
                f"""{Style.BRIGHT}{Fore.RED}{caller_func}(){Style.RESET_ALL} at {
                    timestamp}"""
            )

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
            filename_with_ext = f'{filename}.yml'
            file_path = os.path.join(self.project_root, ".ghost", filename_with_ext)
            try:
                with open(file_path, 'r') as file:
                    etch_from_file = yaml.safe_load(file)
                    for shade_file, etch_file in etch_from_file.items():
                        shade_cls = ShadeRegistry.get_shade_class(self.shade[shade_file])
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
        print(
            f"""\n{Style.BRIGHT}{Fore.CYAN}{
                self.title}{Style.RESET_ALL}"""
        )
        formatted_echoes = ShadeRegistry.get_shade_class(self.shade.TODO)._format_echoes(echo_mask)
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
                formatted_echoes = self._format_echoes(echo_mask)
                filtered_etches = {
                    etch
                    for etch in filtered_etches
                    if any(echo in etch[5] for echo in formatted_echoes)
                }

        sorted_etches = sorted(filtered_etches, key=lambda x: x[0].value)

        # Print etchs
        for etch_shade, etch, file, line, func, echoes in sorted_etches:
            print("\n" + self._format_etch(etch_shade, etch, file, line, func, echoes))

            # * log to the file
            if self.log_to_file:
                self.logger.debug(
                    f"[{etch_shade.name}] - {etch} - {file}:{line} in {func}"
                )

        # Caller information
        caller_frame = inspect.stack()[1]
        caller_file = os.path.relpath(caller_frame.filename, start=self.project_root)
        caller_line = caller_frame.lineno

        print(
            f"""\n{Fore.CYAN}Printed{Style.RESET_ALL} from: {Fore.RED}{caller_file}{
                Style.RESET_ALL} at line {Fore.YELLOW}{caller_line}{Style.RESET_ALL}"""
        )
        print(
            f"{Fore.RED + Style.BRIGHT}Review completed etchs and remove them as necessary.{Style.RESET_ALL}\n"
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
        background_colors = [
            Back.BLACK,
            Back.RED,
            Back.GREEN,
            Back.YELLOW,
            Back.BLUE,
            Back.MAGENTA,
            Back.CYAN,
            Back.WHITE,
            Back.LIGHTBLACK_EX,
            Back.LIGHTRED_EX,
            Back.LIGHTGREEN_EX,
            Back.LIGHTYELLOW_EX,
            Back.LIGHTBLUE_EX,
            Back.LIGHTMAGENTA_EX,
            Back.LIGHTCYAN_EX,
            Back.LIGHTWHITE_EX,
        ]
        colors = {
            self.shade.TODO: Fore.YELLOW,
            self.shade.DEBUG: Fore.BLUE,
            self.shade.INFO: Fore.MAGENTA,
            self.shade.WARN: Fore.RED,
            self.shade.ERROR: Fore.RED + Style.BRIGHT,
            self.shade._ECHO: random.choice(background_colors) + Style.BRIGHT,
        }

        # Choose the color for the shade
        color = colors.get(shade, Style.RESET_ALL)

        if text == "":
            return f"{color}{shade.name}{Style.RESET_ALL}"
        else:
            return f"{color}{text}{Style.RESET_ALL}"

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


    def _format_etch(self, etch_shade, etch, file, line, func, echoes) -> str:
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
            colored_echoes = (
                " ".join(
                    self._color_text(self.shade._ECHO, " " + echo + " ")
                    for echo in echoes
                )
                + "\n"
            )

        else:
            colored_echoes = ""
        etch += "\n"

        return f"[{colored_shade}] {etch}{colored_echoes}(Ln:{self._color_text(etch_shade, line)} - {func} in {path}/{colored_filename})"

    def _setup_logger(self, log_file, log_level=logging.DEBUG):
        """
        Sets up a logger that logs messages to a specified file in a logs directory at the project root.
        """
        # Get the project root by navigating up from the current file's directory
        base_dir = self.project_root

        # Define the path for the logs directory at the project root
        log_dir = os.path.join(base_dir, ".ghost", "logs")

        # Ensure the logs directory exists
        os.makedirs(log_dir, exist_ok=True)

        # Define the full path for the log file
        log_file_path = os.path.join(log_dir, log_file)

        # Set up logging
        self.logger = logging.getLogger(__name__)

        # Avoid adding duplicate handlers
        if not self.logger.hasHandlers():
            self.logger.setLevel(log_level)

            # File handler to output logs to the specified file
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setLevel(log_level)

            # Formatter including timestamp, level, and message
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)

            # Add the handler to the logger
            self.logger.addHandler(file_handler)


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
