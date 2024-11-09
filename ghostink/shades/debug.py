from .base import BaseEtch


class Debug(BaseEtch):
    def __init__(self, ghost_ink) -> None:
        self.DEBUG = ghost_ink.shade.DEBUG
        super().__init__(ghost_ink)

    def dropper(self, etch_obj):
        print(etch_obj)