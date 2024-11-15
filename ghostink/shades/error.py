from .base import BaseEntry
from rich import print, pretty
from rich.console import Console

pretty.install()
console = Console(stderr=True)

class Error(BaseEntry):
    def __init__(self, ghost_ink) -> None:
        self.ERROR = ghost_ink.shade.ERROR
        super().__init__(ghost_ink)

    def dropper(self, entry_obj):
        pass
        # console.print('this is from ERROR')
        # print(entry_obj)
