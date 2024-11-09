from .base import BaseEtch


class Warn(BaseEtch):
    def __init__(self, ghost_ink) -> None:
        self.WARN = ghost_ink.shade.WARN
        super().__init__(ghost_ink)

    def dropper(self, etch_obj):
        print(etch_obj)
