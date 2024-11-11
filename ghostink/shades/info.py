from .base import BaseEtch
from rich import print, pretty

pretty.install()


class Info(BaseEtch):
    def __init__(self, ghost_ink) -> None:
        self.INFO = ghost_ink.shade.INFO
        super().__init__(ghost_ink)

    def dropper(self, etch_obj):
        print(etch_obj)