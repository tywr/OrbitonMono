from math import atan, sin
from glyph import Glyph
from shapes.polygon import draw_polygon
from shapes.parallelogramm import draw_parallelogramm


class LowercaseXGlyph(Glyph):
    name = "lowercase_x"
    unicode = "0x78"
    offset = 0
    width_ratio = 1.2

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, width_ratio=self.width_ratio)
        draw_parallelogramm(pen, dc.stroke, b.x1, b.y1, b.x2, b.y2)
        draw_parallelogramm(
            pen, dc.stroke, b.x2, b.y1, b.x1, b.y2, direction="top-left"
        )
