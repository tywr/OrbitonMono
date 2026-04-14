from math import tan, pi
from glyphs.uppercase import UppercaseGlyph
from draw.parallelogramm import draw_parallelogramm
from draw.rect import draw_rect


class UppercaseVGlyph(UppercaseGlyph):
    name = "uppercase_v"
    unicode = "0x56"
    offset = 0
    overlap = 0.175
    width_ratio = 1.3

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, width_ratio=self.width_ratio, height="cap"
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio
        ov = self.overlap * sx

        theta, delta = draw_parallelogramm(
            pen,
            sx,
            sy,
            b.xmid - ov,
            0,
            b.x2,
            b.y2,
        )
        draw_parallelogramm(
            pen,
            sx,
            sy,
            b.xmid + ov,
            0,
            b.x1,
            b.y2,
            direction="top-left",
        )

        # Fill the gap
        h = dc.gap / (2 * tan(0.5 * pi - theta))
        p = ov * tan(theta)
        draw_rect(
            pen,
            b.xmid - ov,
            b.y1,
            b.xmid + ov,
            b.y1 + p + h,
        )
