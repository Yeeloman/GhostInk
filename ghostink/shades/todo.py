from .base import Baseentry
from rich import print, pretty

pretty.install()

class Todo(Baseentry):
    def __init__(self, ghost_ink) -> None:
        self.TODO = ghost_ink.shade.TODO
        super().__init__(ghost_ink)

    def dropper(self, entry_obj):
        print(entry_obj)