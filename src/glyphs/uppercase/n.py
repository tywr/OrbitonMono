from glyphs.uppercase import UppercaseGlyph
from draw.rect import draw_rect
from draw.parallelogramm import draw_parallelogramm_vertical
from utils.pens import NullPen


class UppercaseNGlyph(UppercaseGlyph):
    name = "uppercase_n"
    unicode = "0x4E"
    offset = 0
    middle_stroke_ratio = 0.9
    overlap = 0.3

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            width_ratio=self.width_ratio,
            uppercase=True,
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio

        # Vertical stems
        draw_rect(pen, b.x1, b.y1, b.x1 + sx, b.y2)
        draw_rect(pen, b.x2 - sx, b.y1, b.x2, b.y2)

        # Diagonal
        theta, delta = draw_parallelogramm_vertical(
            pen,
            sx * self.middle_stroke_ratio,
            sy * self.middle_stroke_ratio,
            b.x2 - sx - dc.gap,
            b.y1,
            b.x1 + sx + dc.gap,
            b.y2,
            direction="top-left",
        )

        # Gaps
        draw_rect(pen, b.x1 + sx, b.y2 - delta, b.x1 + sx + dc.gap, b.y2)
        draw_rect(pen, b.x2 - sx - dc.gap, b.y1, b.x2 - sx, b.y1 + delta)
