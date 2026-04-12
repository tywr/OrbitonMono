from math import tan, pi
from glyphs import Glyph
from draw.parallelogramm import draw_parallelogramm
from draw.rect import draw_rect


class LowercaseVGlyph(Glyph):
    name = "lowercase_v"
    unicode = "0x76"
    offset = 0
    width_ratio = 1.15
    overlap = 0.225

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, width_ratio=self.width_ratio)
        ov = self.overlap * dc.stroke_x

        theta, delta = draw_parallelogramm(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.xmid - ov,
            0,
            b.x2,
            b.y2,
        )
        draw_parallelogramm(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.xmid + ov,
            0,
            b.x1,
            b.y2,
            direction="top-left",
        )

        # Fill the gap
        h = dc.gap / (2 * tan(0.5 * pi - theta))
        p = ov * tan(theta)
        print(b.y1 + p + h)
        draw_rect(
            pen,
            b.xmid - ov,
            b.y1,
            b.xmid + ov,
            b.y1 + p + h,
        )
