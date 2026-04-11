from abc import ABC, abstractmethod
from config import FontConfig as fc


class Glyph(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def unicode(self) -> str: ...

    @property
    @abstractmethod
    def offset(self) -> int: ...

    number_characters: int = 1

    @abstractmethod
    def draw(self, pen, dc) -> None: ...


class LigatureGlyph(Glyph):
    """Base class for ligature glyphs.

    Subclasses must define `components` — a list of glyph names that
    this ligature replaces (e.g. ["low_line", "low_line"] for "__").
    """

    unicode = None
    offset = 0

    @property
    @abstractmethod
    def components(self) -> list[str]: ...
