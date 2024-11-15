from rich import pretty
from rich.text import Text
from .base import BaseEntry
from itertools import chain
from rich.console import Console

pretty.install()
console = Console()

class Todo(BaseEntry):
    def __init__(self, ghost_ink) -> None:
        self.TODO = ghost_ink.shade.TODO
        super().__init__(ghost_ink)

    def dropper(self, entry_obj):
        shade = self.TODO
        for item in entry_obj:
            entry = Text('')
            entry.append(f'{item['title']}\n')
            entry.append(f'{item['description']}\n')
            formatted_tags = self._format_tags(item['tags'])
            relative_path, line_no, func_name = self.ghost_ink._get_relative_path()

            formatted_entry = (
                shade,
                str(entry),
                relative_path,
                line_no,
                func_name,
                formatted_tags,
            )

            if formatted_entry not in self.ghost_ink.entries:
                self.ghost_ink.entries.add(formatted_entry)