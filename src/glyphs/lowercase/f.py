from glyphs import Glyph
from draw.corner import draw_corner
from draw.rect import draw_rect


class LowercaseFGlyph(Glyph):
    name = "lowercase_f"
    unicode = "0x66"
    offset = -28
    rl_ratio = 0.6
    bar_height = 490

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, height="x_height")
        right_len = b.width * self.rl_ratio - dc.stroke_x / 2
        left_len = b.width * (1 - self.rl_ratio) - dc.stroke_x / 2

        # Stem
        draw_rect(pen, b.xmid - dc.stroke_x / 2, 0, b.xmid + dc.stroke_x / 2, dc.x_height)
        # Cross-bar
        draw_rect(
            pen,
            b.xmid - left_len - dc.stroke_x / 2,
            self.bar_height - dc.stroke_y,
            b.xmid + right_len + dc.stroke_x / 2,
            self.bar_height,
        )
        # Corner
        draw_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.xmid - dc.stroke_x / 2,
            dc.x_height,
            b.xmid + right_len + dc.stroke_x / 2,
            dc.ascent,
            right_len + dc.stroke_x,
            dc.ascent - dc.x_height,
            orientation="top-right",
        )
