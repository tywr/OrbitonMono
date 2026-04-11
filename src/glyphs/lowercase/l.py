from glyphs import Glyph
from draw.rect import draw_rect


class LowercaseLGlyph(Glyph):
    name = "lowercase_l"
    unicode = "0x6C"
    offset = 18
    width_ratio = 1.08
    cap = 0.5

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="ascent", width_ratio=self.width_ratio
        )
        right_len = 0.5 * b.width - dc.stroke_x / 2
        left_len = 0.5 * b.width - dc.stroke_x / 2

        # Stem
        draw_rect(pen, b.xmid - dc.stroke_x / 2, 0, b.xmid + dc.stroke_x / 2, dc.ascent)

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
            dc.ascent - dc.stroke_y,
            b.xmid,
            dc.ascent,
        )
