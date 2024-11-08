import traceback
from colorama import Fore, Back, Style, init


class BaseEtch:
    def __init__(self, ghost_ink):
        self.ghost_ink = ghost_ink

    def inker(self, etch_input, shade, echoes) -> None:
        """
        Add a etch with specified text and shade to the Debugger's
        etch list if it's not already present.

        Parameters:
        - etch_input (str or dict or object): The text or object to be added as a etch.
        - shade (GhostInk.shade): The shade of the etch (default: GhostInk.shade.TODO).
        - Echoes: (List of str): Tags added to the etch (task) for customized filtering
        If etch_input is a dictionary or object, it is formatted using _format_etch_from_object method.
        The relative path, line number, and function name of the caller are obtained using _get_relative_path method.
        If shade is ERROR or DEBUG, stack trace is added to the etch text.
        The etch is added to the etch list if it's not already present.
        """
        if shade == self.ghost_ink.shade._ECHO:
            raise ValueError(
                "Attempted to use shade '_ECHO', which is not allowed for etch addition."
            )

        if isinstance(etch_input, str):
            etch_text = etch_input
        else:
            etch_text = self.ghost_ink._format_etch_from_object(etch_input)

        relative_path, line_no, func_name = self.ghost_ink._get_relative_path()

        if shade in [
            self.ghost_ink.shade.ERROR,
            self.ghost_ink.shade.DEBUG,
            self.ghost_ink.shade.WARN,
        ]:
            stack_trace = traceback.format_stack()
            colored_stack_trace = "".join(
                f"{Style.BRIGHT}{Fore.RED + Style.DIM}{line}{Style.RESET_ALL}"
                for line in stack_trace
            )
            etch_text += f"\nStack Trace:\n{colored_stack_trace}"

        formatted_echoes = self.ghost_ink._format_echoes(echoes)
        formatted_etch = (
            shade,
            etch_text,
            relative_path,
            line_no,
            func_name,
            formatted_echoes,
        )

        if formatted_etch not in self.ghost_ink.etches:
            self.ghost_ink.etches.add(formatted_etch)
