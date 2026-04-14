from glyphs.uppercase import UppercaseGlyph
from draw.rect import draw_rect


class UppercaseTGlyph(UppercaseGlyph):
    name = "uppercase_t"
    unicode = "0x54"
    offset = 0
    width_ratio = 1.2

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="cap", width_ratio=self.width_ratio
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio

        # Vertical stem (centered)
        draw_rect(pen, b.xmid - sx / 2, b.y1, b.xmid + sx / 2, b.y2)
        # Top bar
        draw_rect(pen, b.x1, b.y2 - sy, b.x2, b.y2)
