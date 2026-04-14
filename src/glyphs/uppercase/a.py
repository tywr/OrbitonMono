from math import cos
from glyphs.uppercase import UppercaseGlyph
from draw.parallelogramm import draw_parallelogramm
from draw.rect import draw_rect


class UppercaseAGlyph(UppercaseGlyph):
    name = "uppercase_a"
    unicode = "0x41"
    offset = 0
    width_ratio = 1.25
    bar_height = 320
    overlap = 0.05

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="cap", width_ratio=self.width_ratio
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio

        half_width = b.width / 2 - sx / 2
        ov = self.overlap * b.width
        # Left branch
        draw_parallelogramm(
            pen,
            sx,
            sy,
            b.x2,
            b.y1,
            b.xmid - ov,
            b.y2,
            direction="top-left",
        )
        # Right branch
        theta, delta = draw_parallelogramm(
            pen, sx, sy, b.x1, b.y1, b.xmid + ov, b.y2
        )
        # Crossbar
        draw_rect(
            pen,
            b.xmid - half_width + (self.bar_height - sy) * cos(theta),
            self.bar_height - sy,
            b.xmid + half_width - (self.bar_height - sy) * cos(theta),
            self.bar_height,
        )
