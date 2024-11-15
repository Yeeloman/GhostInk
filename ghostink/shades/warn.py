from .base import BaseEntry
from rich import print, pretty

pretty.install()


class Warn(BaseEntry):
    def __init__(self, ghost_ink) -> None:
        self.WARN = ghost_ink.shade.WARN
        super().__init__(ghost_ink)

    def dropper(self, entry_obj):
        print(entry_obj)
