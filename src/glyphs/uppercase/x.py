from math import tan
from glyphs.uppercase import UppercaseGlyph
from draw.parallelogramm import draw_parallelogramm
from draw.rect import draw_rect


class UppercaseXGlyph(UppercaseGlyph):
    name = "uppercase_x"
    unicode = "0x58"
    offset = 0
    width_ratio = 1.25

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, width_ratio=self.width_ratio, height="cap"
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio

        draw_parallelogramm(pen, sx, sy, b.x1, b.y1, b.x2, b.y2)
        theta, delta = draw_parallelogramm(
            pen, sx, sy, b.x2, b.y1, b.x1, b.y2, direction="top-left"
        )

        # Fill the gaps
        h = tan(theta) * dc.gap / 2
        epsilon = tan(theta) * delta / 2

        draw_rect(
            pen,
            b.xmid - dc.gap / 2,
            b.ymid + epsilon,
            b.xmid + dc.gap / 2,
            b.ymid + epsilon + h,
        )
        draw_rect(
            pen,
            b.xmid - dc.gap / 2,
            b.ymid - epsilon - h,
            b.xmid + dc.gap / 2,
            b.ymid - epsilon,
        )
