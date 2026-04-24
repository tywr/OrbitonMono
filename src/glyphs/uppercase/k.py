from math import tan
from glyphs.uppercase import UppercaseGlyph
from draw.rect import draw_rect
from draw.parallelogramm import draw_parallelogramm


class UppercaseKGlyph(UppercaseGlyph):
    name = "uppercase_k"
    unicode = "0x4B"
    offset = 38
    branch_ratio = 0.68
    width_ratio = 1.08
    mid_ratio = 0.53
    upper_branch_offset = 0.01

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, width_ratio=self.width_ratio, height="cap"
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio
        x_branch = b.x1 + (1 - self.branch_ratio) * b.width
        xtop = b.x2 - self.upper_branch_offset * b.width
        ymid = b.y1 + self.mid_ratio * b.height

        # Left ascender stem
        draw_rect(pen, b.x1, 0, b.x1 + sx, dc.cap)

        draw_parallelogramm(
            pen,
            sx,
            sy,
            x_branch,
            ymid + sy / 2,
            b.x2,
            b.y1,
            direction="bottom-right",
        )

        # Upper branch
        theta, delta = draw_parallelogramm(
            pen,
            sx,
            sy,
            x_branch,
            ymid - sy / 2,
            xtop,
            b.y2,
        )

        # Neck
        draw_rect(
            pen,
            b.x1,
            ymid - sy / 2,
            x_branch + delta / tan(theta),
            ymid + sy / 2,
        )
