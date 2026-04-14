from math import tan
from glyphs.uppercase import UppercaseGlyph
from draw.rect import draw_rect
from draw.parallelogramm import draw_parallelogramm


class LowercaseKGlyph(UppercaseGlyph):
    name = "uppercase_k"
    unicode = "0x4B"
    offset = 28
    neck_len = 100
    branch_ratio = 0.75
    width_ratio = 1.22

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, width_ratio=self.width_ratio, height="cap"
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio
        x_branch = b.x1 + (1 - self.branch_ratio) * b.width

        # Left ascender stem
        draw_rect(pen, b.x1, 0, b.x1 + sx, dc.cap)

        # Upper branch
        draw_parallelogramm(
            pen,
            sx,
            sy,
            x_branch,
            b.ymid + sy / 2,
            b.x2,
            b.y1,
            direction="bottom-right",
        )
        theta, delta = draw_parallelogramm(
            pen,
            sx,
            sy,
            x_branch,
            b.ymid - sy / 2,
            b.x2,
            b.y2,
        )

        # Neck
        draw_rect(
            pen,
            b.x1,
            b.ymid - sy / 2,
            x_branch + delta / tan(theta),
            b.ymid + sy / 2,
        )
