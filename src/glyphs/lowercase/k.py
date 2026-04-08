from math import tan
from glyphs import Glyph
from draw.rect import draw_rect
from draw.parallelogramm import draw_parallelogramm


class LowercaseKGlyph(Glyph):
    name = "lowercase_k"
    unicode = "0x6B"
    offset = 28
    bowl_width = 320
    neck_len = 100
    width_ratio = 1.06
    branch_ratio = 0.75

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, width_ratio=self.width_ratio)
        x_branch = b.x1 + (1 - self.branch_ratio) * b.width

        # Left ascender stem
        draw_rect(pen, b.x1, 0, b.x1 + dc.stroke_x, dc.ascent)

        # Upper branch
        draw_parallelogramm(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            x_branch,
            b.ymid + dc.stroke_y / 2,
            b.x2,
            b.y1,
            direction="bottom-right",
        )
        theta, delta = draw_parallelogramm(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            x_branch,
            b.ymid - dc.stroke_y / 2,
            b.x2,
            b.y2,
        )

        # Neck
        draw_rect(
            pen,
            b.x1,
            b.ymid - dc.stroke_y / 2,
            x_branch + delta / tan(theta),
            b.ymid + dc.stroke_y / 2,
        )
