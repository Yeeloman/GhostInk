from .base import Baseentry
from rich import print, pretty

pretty.install()


class Warn(Baseentry):
    def __init__(self, ghost_ink) -> None:
        self.WARN = ghost_ink.shade.WARN
        super().__init__(ghost_ink)

    def dropper(self, entry_obj):
        print(entry_obj)
