from glyphs.uppercase import UppercaseGlyph
from draw.rect import draw_rect


class UppercaseLGlyph(UppercaseGlyph):
    name = "uppercase_l"
    unicode = "0x4C"
    offset = 18

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="cap", width_ratio=self.width_ratio
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio

        # Vertical stem
        draw_rect(pen, b.x1, b.y1, b.x1 + sx, b.y2)
        # Bottom bar
        draw_rect(pen, b.x1, b.y1, b.x2, b.y1 + sy)
