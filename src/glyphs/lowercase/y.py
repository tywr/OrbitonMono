from math import tan
from glyph import Glyph
from shapes.parallelogramm import draw_parallelogramm


class LowercaseYGlyph(Glyph):
    name = "lowercase_y"
    unicode = "0x79"
    offset = 0
    width_ratio = 1.2
    overlap = 0.05
    dent_ratio = 0.1

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, width_ratio=self.width_ratio)
        dent_height = self.dent_ratio * b.height

        draw_parallelogramm(
            pen,
            dc.stroke,
            b.xmid + self.overlap * b.width,
            dent_height,
            b.x1,
            b.y2,
            direction="top-left",
        )
        theta, delta = draw_parallelogramm(
            pen,
            dc.stroke,
            b.xmid - self.overlap * b.width,
            dent_height,
            b.x2,
            b.y2,
        )
        draw_parallelogramm(
            pen,
            dc.stroke,
            b.xmid - self.overlap * b.width + delta,
            dent_height,
            b.xmid
            - self.overlap * b.width
            - (abs(dc.descent) + dent_height) / tan(theta),
            dc.descent,
            direction="bottom-left",
        )
