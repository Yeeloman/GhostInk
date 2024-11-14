from .base import Baseentry
from rich import print, pretty

pretty.install()


class Error(Baseentry):
    def __init__(self, ghost_ink) -> None:
        self.ERROR = ghost_ink.shade.ERROR
        super().__init__(ghost_ink)

    def dropper(self, entry_obj):
        print(entry_obj)
