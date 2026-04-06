from abc import ABC
from glyphs import Glyph


class UppercaseGlyph(Glyph, ABC):
    """Define common class variables for all uppercase glyphs"""

    width_ratio = 1.08
