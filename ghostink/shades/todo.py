from .base import BaseEtch
from rich import print, pretty

pretty.install()

class Todo(BaseEtch):
    def __init__(self, ghost_ink) -> None:
        self.TODO = ghost_ink.shade.TODO
        super().__init__(ghost_ink)

    def dropper(self, etch_obj):
        print(etch_obj)