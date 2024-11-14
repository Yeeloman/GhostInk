from typing import List
from rich import pretty

pretty.install()


class Baseentry:
    def __init__(self, ghost_ink):
        self.ghost_ink = ghost_ink

    def inker(self, entry_input, shade, tags, **kwargs) -> None:
        """
        Add a entry with specified text and shade to the Debugger's
        entry list if it's not already present.

        Parameters:
        - entry_input (str or dict or object): The text or object to be added as a entry.
        - shade (GhostInk.shade): The shade of the entry (default: GhostInk.shade.TODO).
        - tags: (List of str): Tags added to the entry (task) for customized filtering
        If entry_input is a dictionary or object, it is formatted using _format_entry_from_object method.
        The relative path, line number, and function name of the caller are obtained using _get_relative_path method.
        If shade is ERROR or DEBUG, stack trace is added to the entry text.
        The entry is added to the entry list if it's not already present.
        """
        if shade == self.ghost_ink.shade._tag:
            raise ValueError(
                "Attempted to use shade '_tag', which is not allowed for entry addition."
            )

        if isinstance(entry_input, str):
            entry_text = entry_input
        else:
            entry_text = self.ghost_ink._format_entry_from_object(entry_input)

        relative_path, line_no, func_name = self.ghost_ink._get_relative_path()

        formatted_tags = self._format_tags(tags)
        formatted_entry = (
            shade,
            entry_text,
            relative_path,
            line_no,
            func_name,
            formatted_tags,
        )

        if formatted_entry not in self.ghost_ink.entries:
            self.ghost_ink.entries.add(formatted_entry)

    def _format_tags(self, tags: List[str] = []) -> tuple:
        if not tags:
            return ()

        formatted_tags = []

        for tag in tags:
            if "#" in tag:
                continue
            spaceless_tag = tag.strip()
            formatted_tag = spaceless_tag.replace(" ", "_")
            formatted_tag = f"#{formatted_tag}"
            formatted_tags.append(formatted_tag)

        return tuple(formatted_tags)
