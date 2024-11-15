from .base import BaseEntry
from rich import print, pretty

pretty.install()


class Debug(BaseEntry):
    def __init__(self, ghost_ink) -> None:
        self.DEBUG = ghost_ink.shade.DEBUG
        super().__init__(ghost_ink)

    def dropper(self, entry_obj):
        print(entry_obj)