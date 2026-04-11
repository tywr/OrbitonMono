from abc import ABC
from glyphs import Glyph


class NumberGlyph(Glyph, ABC):
    """Define common class variables for all number glyphs"""

    width_ratio = 1.08
