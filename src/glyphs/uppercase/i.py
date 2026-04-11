from glyphs.uppercase import UppercaseGlyph
from draw.rect import draw_rect


class UppercaseIGlyph(UppercaseGlyph):
    name = "uppercase_i"
    unicode = "0x49"
    offset = 0

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="cap", width_ratio=self.width_ratio
        )

        # Vertical stem (centered)
        draw_rect(pen, b.xmid - dc.stroke_x / 2, b.y1, b.xmid + dc.stroke_x / 2, b.y2)
        # Top bar
        draw_rect(pen, b.x1, b.y2 - dc.stroke_y, b.x2, b.y2)
        # Bottom bar
        draw_rect(pen, b.x1, b.y1, b.x2, b.y1 + dc.stroke_y)
