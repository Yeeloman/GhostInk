from .base import BaseEtch


class Info(BaseEtch):
    def __init__(self, ghost_ink) -> None:
        super().__init__(ghost_ink)

    def inker(self, etch_input, shade, echoes, **kwargs):
        if isinstance(etch_input, dict) and "title" in etch_input:
            pass
        else:
            super().inker(etch_input, shade, echoes, **kwargs)
