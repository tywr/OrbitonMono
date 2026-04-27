from abc import ABC
from glyphs import Glyph


class UppercaseGlyph(Glyph, ABC):
    """Define common class variables for all uppercase glyphs"""

    width_ratio = 1.00
    stroke_x_ratio = 1.00
    stroke_y_ratio = 1.18
