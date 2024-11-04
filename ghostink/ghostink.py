import os
import traceback
import json
import inspect
import logging
from datetime import datetime
from enum import Enum
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


class GhostInk:
    """
    Prints file name, line number, function name, and timestamp of the method call.
    """

    class mode(Enum):
        """
        Defines an Enum class 'mode' with options:
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

    def __init__(
        self,
        title: str = "GhostInk",
        project_root: str = ".",
        log_to_file: bool = False,
        log_file: str = "etchara.log"
    ):
        self.title = title
        self.etchings = set()
        self.project_root = project_root
        self.log_to_file = log_to_file
        self.log_file = log_file
        self.logger = None

        if log_to_file:
            self._setup_logger(log_file)

    def _setup_logger(self, log_file, log_level=logging.DEBUG):
        """
        Sets up a logger that logs messages to a specified file in a logs directory at the project root.
        """
        # Get the project root by navigating up from the current file's directory
        base_dir = self.project_root

        # Define the path for the logs directory at the project root
        log_dir = os.path.join(base_dir, "logs")

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
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)

            # Add the handler to the logger
            self.logger.addHandler(file_handler)

    def haunt(self, msg: str = None) -> None:
        """
        Prints the file name, line number, function name, and timestamp of where this method is called.

        Parameters:
        - msg (str): Optional message to print before the file information.

        Prints the file information along with the message if provided, including the file name, line number, function name, and timestamp.
        """
        # Get the calling frame information
        caller_frame = inspect.stack()[1]
        caller_file = os.path.basename(caller_frame.filename)  # File name
        caller_line = caller_frame.lineno  # Line number
        caller_func = caller_frame.function  # Function name

        # Get the current timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")  # Time down to milliseconds

        if msg:
            print(msg)
            print(
                f"{Style.BRIGHT}{Fore.YELLOW}└── {
                    caller_file}{Style.RESET_ALL}:"
                f"{Style.BRIGHT}{Fore.MAGENTA}{
                    caller_line}{Style.RESET_ALL} in "
                f"{Style.BRIGHT}{Fore.RED}{caller_func}(){Style.RESET_ALL} at {
                    timestamp}"
            )
        else:
            print(
                f"{Style.BRIGHT}{Fore.YELLOW}{caller_file}{Style.RESET_ALL}:"
                f"{Style.BRIGHT}{Fore.MAGENTA}{
                    caller_line}{Style.RESET_ALL} in "
                f"{Style.BRIGHT}{Fore.RED}{caller_func}(){Style.RESET_ALL} at {
                    timestamp}"
            )

    def inkdrop(self, etch_input: any, mode: mode = mode.TODO) -> None:
        """
        Add a etch with specified text and mode to the Debugger's
        etch list if it's not already present.

        Parameters:
        - etch_input (str or dict or object): The text or object to be added as a etch.
        - mode (GhostInk.mode): The mode of the etch (default: GhostInk.mode.TODO).

        If etch_input is a dictionary or object, it is formatted using _format_etch_from_object method.
        The relative path, line number, and function name of the caller are obtained using _get_relative_path method.
        If mode is ERROR or DEBUG, stack trace is added to the etch text.
        The etch is added to the etch list if it's not already present.
        """
        if isinstance(etch_input, str):
            etch_text = etch_input
        else:
            etch_text = self._format_etch_from_object(etch_input)

        relative_path, line_no, func_name = self._get_relative_path()

        if mode in [self.mode.ERROR, self.mode.DEBUG, self.mode.WARN]:
            stack_trace = traceback.format_stack()
            colored_stack_trace = "".join(
                f"{Style.BRIGHT}{Fore.RED + Style.DIM}{line}{Style.RESET_ALL}"
                for line in stack_trace
            )
            etch_text += f"\nStack Trace:\n{colored_stack_trace}"

        formatted_etch = (mode, etch_text, relative_path, line_no, func_name)

        if formatted_etch not in self.etchings:
            self.etchings.add(formatted_etch)

    def whisper(self, mode_mask: str = None, file_mask: str = None) -> None:
        """
        Prints filtered and sorted etchs based on the provided mode_mask and file_mask.

        Parameters:
        - mode_mask (GhostInk.mode): The mode to filter etchs by (default: None).
        - file_mask (str): The filename to filter etchs by (default: None).
        """
        # Display Title
        print(f"\n{Style.BRIGHT}{Fore.CYAN}{
              self.title:^23}{Style.RESET_ALL}\n")

        # Filter and sort etchs
        filtered_etchings = [
            etch
            for etch in self.etchings
            if (mode_mask is None or etch[0] == mode_mask)
            and (file_mask is None or etch[2] == file_mask)
        ]
        sorted_etchings = sorted(filtered_etchings, key=lambda x: x[0].value)

        # Print etchs
        for etch_mode, etch, file, line, func in sorted_etchings:
            print(self._format_etch(etch_mode, etch, file, line, func))
            if self.log_to_file:
                self.logger.debug(
                    f"[{etch_mode.name}] - {etch} - {file}:{line} in {func}")

        # Caller information
        caller_frame = inspect.stack()[1]
        caller_file = os.path.relpath(
            caller_frame.filename, start=self.project_root)
        caller_line = caller_frame.lineno

        print(
            f"\n{Fore.CYAN}Printed{Style.RESET_ALL} from: {Fore.RED}{caller_file}{
                Style.RESET_ALL} at line {Fore.YELLOW}{caller_line}{Style.RESET_ALL}"
        )
        print(
            f"{Fore.RED + Style.BRIGHT}Review completed etchs and remove them as necessary.{Style.RESET_ALL}\n"
        )

    def _color_text(self, mode: mode, text: str = "") -> None:
        """
        Color the text based on the debug mode using colorama.

        Parameters:
        - text (str): The text to color.
        - mode (self.mode): The mode that determines the color.

        Returns:
        - str: Colored text.
        """
        colors = {
            self.mode.TODO: Fore.YELLOW,
            self.mode.DEBUG: Fore.BLUE,
            self.mode.INFO: Fore.MAGENTA,
            self.mode.WARN: Fore.RED,
            self.mode.ERROR: Fore.RED + Style.BRIGHT,
        }

        # Choose the color for the mode
        color = colors.get(mode, Style.RESET_ALL)

        if text == "":
            return f"{color}{mode.name}{Style.RESET_ALL}"
        else:
            return f"{color}{text}{Style.RESET_ALL}"

    def _get_relative_path(self) -> tuple[str, int, str]:
        """
        Return the relative path and line number of the code file
        calling this method, relative to the project's base directory.
        """
        caller_frame = inspect.stack()[2]
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
        if isinstance(etch_input, dict):
            # Pretty-print dictionaries
            return json.dumps(etch_input, indent=4)
        elif isinstance(etch_input, (list, tuple)):
            # Join list/tuple elements
            return ", ".join(str(item) for item in etch_input)
        elif isinstance(etch_input, set):
            # Display sets
            return "{" + ", ".join(str(item) for item in etch_input) + "}"
        elif isinstance(etch_input, str):
            return etch_input  # Directly return strings
        elif hasattr(etch_input, "__dict__"):
            # Format custom objects using their attributes
            return ", ".join(
                f"{key}: {value}" for key, value in vars(etch_input).items()
            )
        else:
            # Handle other data types or raise a warning
            return str(etch_input)  # Convert any other type to string

    def _format_etch(self, mode, etch, file, line, func) -> str:
        """
        Formats a etch for printing.

        Parameters:
        - etch (tuple): The etch tuple to format.

        Returns:
        - str: The formatted string.
        """
        return f"[{self._color_text(mode)}] {etch}\n(Ln:{self._color_text(mode, line)} - {func} in {file})"


__all__ = ["GhostInk"]
