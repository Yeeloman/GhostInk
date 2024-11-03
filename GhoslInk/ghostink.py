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
        - TODO: Represents a task to be done.
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
        log_file: str = "taskara.log"
    ):
        self.title = title
        self.tasks = set()
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

    def set_mode(self, new_mode: mode) -> None:
        """
        Set the mode of the GhostInk instance to the specified new_mode.

        Parameters:
        - new_mode (GhostInk.mode): The new mode to set for the GhostInk instance.

        If the new_mode is not an instance of GhostInk.mode, the mode is set to GhostInk.mode.TODO.
        """
        if isinstance(new_mode, self.mode):
            self.mode = new_mode
        else:
            self.mode = self.mode.TODO

    def ln(self, msg: str = None) -> None:
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

    def add_task(self, task_input: any, mode: mode = mode.TODO) -> None:
        """
        Add a task with specified text and mode to the Debugger's
        task list if it's not already present.

        Parameters:
        - task_input (str or dict or object): The text or object to be added as a task.
        - mode (GhostInk.mode): The mode of the task (default: GhostInk.mode.TODO).

        If task_input is a dictionary or object, it is formatted using _format_task_from_object method.
        The relative path, line number, and function name of the caller are obtained using _get_relative_path method.
        If mode is ERROR or DEBUG, stack trace is added to the task text.
        The task is added to the task list if it's not already present.
        """
        if isinstance(task_input, str):
            task_text = task_input
        else:
            task_text = self._format_task_from_object(task_input)

        relative_path, line_no, func_name = self._get_relative_path()

        if mode in [self.mode.ERROR, self.mode.DEBUG, self.mode.WARN]:
            stack_trace = traceback.format_stack()
            colored_stack_trace = "".join(
                f"{Style.BRIGHT}{Fore.RED + Style.DIM}{line}{Style.RESET_ALL}"
                for line in stack_trace
            )
            task_text += f"\nStack Trace:\n{colored_stack_trace}"

        formatted_task = (mode, task_text, relative_path, line_no, func_name)

        if formatted_task not in self.tasks:
            self.tasks.add(formatted_task)

    def print(self, filter_mode: str = None, filter_filename: str = None) -> None:
        """
        Prints filtered and sorted tasks based on the provided filter_mode and filter_filename.

        Parameters:
        - filter_mode (GhostInk.mode): The mode to filter tasks by (default: None).
        - filter_filename (str): The filename to filter tasks by (default: None).
        """
        # Display Title
        print(f"\n{Style.BRIGHT}{Fore.CYAN}{
              self.title:^23}{Style.RESET_ALL}\n")

        # Filter and sort tasks
        filtered_tasks = [
            task
            for task in self.tasks
            if (filter_mode is None or task[0] == filter_mode)
            and (filter_filename is None or task[2] == filter_filename)
        ]
        sorted_tasks = sorted(filtered_tasks, key=lambda x: x[0].value)

        # Print tasks
        for task_mode, task, file, line, func in sorted_tasks:
            print(self._format_task(task_mode, task, file, line, func))
            if self.log_to_file:
                self.logger.debug(
                    f"[{task_mode.name}] - {task} - {file}:{line} in {func}")

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
            f"{Fore.RED + Style.BRIGHT}Review completed tasks and remove them as necessary.{Style.RESET_ALL}\n"
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

    def _format_task_from_object(self, task_input: any) -> str:
        """
        Convert a dictionary or object to a string
        representation suitable for a task.

        Parameters:
        - task_input (dict or object): The input to format.

        Returns:
        - str: A formatted string representing the task.
        """
        if isinstance(task_input, dict):
            # Pretty-print dictionaries
            return json.dumps(task_input, indent=4)
        elif isinstance(task_input, (list, tuple)):
            # Join list/tuple elements
            return ", ".join(str(item) for item in task_input)
        elif isinstance(task_input, set):
            # Display sets
            return "{" + ", ".join(str(item) for item in task_input) + "}"
        elif isinstance(task_input, str):
            return task_input  # Directly return strings
        elif hasattr(task_input, "__dict__"):
            # Format custom objects using their attributes
            return ", ".join(
                f"{key}: {value}" for key, value in vars(task_input).items()
            )
        else:
            # Handle other data types or raise a warning
            return str(task_input)  # Convert any other type to string

    def _format_task(self, mode, task, file, line, func) -> str:
        """
        Formats a task for printing.

        Parameters:
        - task (tuple): The task tuple to format.

        Returns:
        - str: The formatted string.
        """
        return f"[{self._color_text(mode)}] {task}\n(Ln:{self._color_text(mode, line)} - {func} in {file})"


__all__ = ["GhostInk"]
