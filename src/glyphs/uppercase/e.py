from glyphs.uppercase import UppercaseGlyph
from draw.rect import draw_rect


class UppercaseEGlyph(UppercaseGlyph):
    name = "uppercase_e"
    unicode = "0x45"
    offset = 0
    mid_bar_ratio = 0.9

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="cap", width_ratio=self.width_ratio, uppercase=True
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio

        # Vertical stem
        draw_rect(pen, b.x1, b.y1, b.x1 + sx, b.y2)

        # Top bar
        draw_rect(pen, b.x1, b.y2 - sy, b.x2, b.y2)

        # Middle bar
        draw_rect(
            pen,
            b.x1,
            b.ymid - sy / 2,
            b.x1 + self.mid_bar_ratio * b.width,
            b.ymid + sy / 2,
        )

        # Bottom bar
        draw_rect(pen, b.x1, b.y1, b.x2, b.y1 + sy)
