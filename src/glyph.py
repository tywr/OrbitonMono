from abc import ABC, abstractmethod


class Glyph(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def unicode(self) -> str: ...

    @abstractmethod
    def draw(self, pen, stroke: int) -> None: ...
