from glyphs import Glyph
from draw.rect import draw_rect


class LowercaseIGlyph(Glyph):
    name = "lowercase_i"
    unicode = "0x69"
    offset = 30
    width_ratio = 1.1
    cap = 0.45
    dot_width = 25

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, width_ratio=self.width_ratio)
        right_len = 0.5 * b.width - dc.stroke_x / 2
        left_len = 0.5 * b.width - dc.stroke_x / 2

        # Stem
        draw_rect(
            pen, b.xmid - dc.stroke_x / 2, 0, b.xmid + dc.stroke_x / 2, dc.x_height
        )
        # Footer
        draw_rect(
            pen,
            b.xmid - left_len - dc.stroke_x / 2,
            0,
            b.xmid + right_len + dc.stroke_x / 2,
            dc.stroke_y,
        )
        # Left cap
        draw_rect(
            pen,
            b.xmid - b.width * self.cap,
            dc.x_height - dc.stroke_y,
            b.xmid,
            dc.x_height,
        )
        # Accent dot
        draw_rect(
            pen,
            b.xmid + dc.stroke_x / 2 - self.dot_width - dc.stroke_x,
            dc.accent - self.dot_width / 2 - dc.stroke_x / 2,
            b.xmid + dc.stroke_x / 2,
            dc.accent + dc.stroke_x / 2 + self.dot_width / 2,
        )
