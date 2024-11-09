from .base import BaseEtch


class Error(BaseEtch):
    def __init__(self, ghost_ink) -> None:
        self.ERROR = ghost_ink.shade.ERROR
        super().__init__(ghost_ink)

    def dropper(self, etch_obj):
        print(etch_obj)
