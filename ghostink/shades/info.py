from .base import BaseEntry
from rich import print, pretty

pretty.install()


class _Info(BaseEntry):
    def __init__(self, ghost_ink) -> None:
        self.INFO = ghost_ink.shade.INFO
        super().__init__(ghost_ink)

    def dropper(self, entry_obj):
        print(entry_obj)