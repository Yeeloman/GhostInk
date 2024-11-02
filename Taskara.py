import os
import traceback
import json
import inspect
from datetime import datetime
from enum import Enum


class Taskara():
    """
    Prints file name, line number, function name, and timestamp of the method call.
    """
    class mode(Enum):
        '''
        Defines an Enum class 'mode' with options:
        - TODO: Represents a task to be done.
        - DEBUG: Represents debug information.
        - INFO: Represents informational messages.
        - WARN: Represents warning messages.
        '''
        TODO = "TODO"
        DEBUG = "DEBUG"
        INFO = "INFO"
        WARN = "WARN"

    def __init__(self, project_root='.'):
        self.tasks = set()
        self.project_root = project_root

    def set_mode(self, new_mode):
        """
        Set the mode of the Taskara instance to the specified new_mode.

        Parameters:
        - new_mode (Taskara.mode): The new mode to set for the Taskara instance.

        If the new_mode is not an instance of Taskara.mode, the mode is set to Taskara.mode.TODO.
        """
        if isinstance(new_mode, self.mode):
            self.mode = new_mode
        else:
            self.mode = self.mode.TODO

    def ln(self, msg: str = None):
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
        timestamp = datetime.now().strftime('%H:%M:%S')  # Time down to milliseconds

        if msg:
            print(msg)
            print(f"\033[1;33m└──{caller_file}\033[0m:\033[1;95m{
                caller_line}\033[0m in \033[1;91m{caller_func}()\033[0m at {timestamp}")
        else:
            print(f"\033[1;33m{caller_file}\033[0m:\033[1;95m{
                caller_line}\033[0m in \033[1;91m{caller_func}()\033[0m at {timestamp}")

    def add_task(self, task_input, mode=mode.TODO):
        """
        Add a task with specified text and mode to the Debugger's
        task list if it's not already present.
        
        Parameters:
        - task_input (str or dict or object): The text or object to be added as a task.
        - mode (Taskara.mode): The mode of the task (default: Taskara.mode.TODO).
        
        If task_input is a dictionary or object, it is formatted using _format_task_from_object method.
        The relative path, line number, and function name of the caller are obtained using _get_relative_path method.
        If mode is WARN or DEBUG, stack trace is added to the task text.
        The task is added to the task list if it's not already present.
        """
        if isinstance(task_input, str):
            task_text = task_input
        else:
            task_text = self._format_task_from_object(task_input)

        relative_path, line_no, func_name = self._get_relative_path()

        if mode in [self.mode.WARN, self.mode.DEBUG]:
            stack_trace = traceback.format_stack()
            task_text += f"\nStack Trace:\n{
                ''.join(stack_trace)}"

        formatted_task = (mode, task_text, relative_path, line_no, func_name)

        if formatted_task not in self.tasks:
            self.tasks.add(formatted_task)

    def print(self, filter_mode=None, filter_filename=None):
        """
        Prints filtered and sorted tasks based on the provided filter_mode and filter_filename.

        Parameters:
        - filter_mode (Taskara.mode): The mode to filter tasks by (default: None).
        - filter_filename (str): The filename to filter tasks by (default: None).
        """
        # Display Title
        title = "TaskManager"
        print(f"\n\033[1;4;36m{title:^23}\033[0m\n")

        # Filter and sort tasks
        filtered_tasks = [
            task for task in self.tasks
            if (filter_mode is None or task[0] == filter_mode) and
            (filter_filename is None or task[2] == filter_filename)
        ]
        sorted_tasks = sorted(filtered_tasks, key=lambda x: x[0].value)

        # Print tasks
        for task_mode, task, file, line, func in sorted_tasks:
            print(self._format_task(task_mode, task, file, line, func))

        # Caller information
        caller_frame = inspect.stack()[1]
        caller_file = os.path.relpath(
            caller_frame.filename, start=self.project_root)
        caller_line = caller_frame.lineno

        print(
            f"\n\033[1;36mPrinted\033[0m from: \033[1;31m{
                caller_file}\033[0m at line \033[1;33m{caller_line}\033[0m"
        )
        print(
            "\033[1;31mReview completed tasks and remove them as necessary.\033[0m\n")

    def _color_text(self, mode, text=""):
        """
        Color the text based on the debug mode.

        Parameters:
        - text (str): The text to color.
        - mode (self.mode): The mode that determines the color.

        Returns:
        - str: Colored text.
        """
        colors = {
            self.mode.TODO: '\033[1;33m',
            self.mode.DEBUG: '\033[1;34m',
            self.mode.INFO: '\033[1;35m',
            self.mode.WARN: '\033[1;31m',
            'reset': '\033[0m'
        }
        if text == "":
            return f"{colors.get(mode, colors['reset'])}{mode.name}{colors['reset']}"
        else:
            return f"{colors.get(mode, colors['reset'])}{text}{colors['reset']}"

    def _get_relative_path(self):
        """
        Return the relative path and line number of the code file
        calling this method, relative to the project's base directory.
        """
        caller_frame = inspect.stack()[2]
        full_path = caller_frame.filename
        relative_path = os.path.relpath(full_path, start=self.project_root)
        return relative_path, caller_frame.lineno, caller_frame.function

    def _format_task_from_object(self, task_input):
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
            return ", ".join(f"{key}: {value}" for key, value in vars(task_input).items())
        else:
            # Handle other data types or raise a warning
            return str(task_input)  # Convert any other type to string

    def _format_task(self, mode, task, file, line, func):
        """
        Formats a task for printing.

        Parameters:
        - task (tuple): The task tuple to format.

        Returns:
        - str: The formatted string.
        """
        return f"[{self._color_text(mode)}] {task}\n(Ln:{self._color_text(mode, line)} - {file} in {func})"


__all__ = ["Taskara"]
