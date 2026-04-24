from abc import ABC, abstractmethod
from config import FontConfig as fc


class Glyph(ABC):
    accent_x_offset: int = 0

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
    font_feature: dict = None
    default_italic: bool = False

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


class ContextualLigatureGlyph(LigatureGlyph):
    """Ligature that only fires when not adjacent to `forbidden_neighbors`.

    Useful for capped-length ligatures: e.g. `==` and `===` ligate, but
    `====` and longer stay unligated. Set `forbidden_neighbors` to the
    glyph names whose presence on either side disqualifies the match
    (typically the ligature's own component glyph).
    """

    forbidden_neighbors: list[str] = []
