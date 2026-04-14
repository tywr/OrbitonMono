from glyphs import Glyph
from draw.rect import draw_rect
from draw.corner import draw_corner


class LowercaseI2Glyph(Glyph):
    name = "lowercase_i_2"
    unicode = "0x69"
    font_feature = {"ss03": 1}
    default_italic = True
    offset = 18
    width_ratio = 1.08
    cap = 0.45
    dot_width = 36
    rl_ratio = 0.5

    def draw_base(self, pen, dc):
        """Draw the letter without the dot (for use with accents)."""
        b = dc.body_bounds(offset=self.offset, width_ratio=self.width_ratio)
        right_len = self.rl_ratio * b.width - dc.stroke_x / 2
        left_len = (1 - self.rl_ratio) * b.width - dc.stroke_x / 2
        ym4 = b.y1 + b.height / 4

        # Stem
        draw_rect(
            pen, b.xmid - dc.stroke_x / 2, ym4, b.xmid + dc.stroke_x / 2, dc.x_height
        )

        draw_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.xmid - dc.stroke_x / 2,
            ym4,
            b.x2,
            b.y1,
            b.width / 2 + dc.stroke_x / 2,
            ym4 - b.y1,
            orientation="bottom-right",
        )
        # Footer
        # draw_rect(
        #     pen,
        #     b.xmid,
        #     0,
        #     b.xmid + right_len + dc.stroke_x / 2,
        #     dc.stroke_y,
        # )
        # Left cap
        draw_rect(
            pen,
            b.xmid - b.width * self.cap,
            dc.x_height - dc.stroke_y,
            b.xmid,
            dc.x_height,
        )

    def draw(self, pen, dc):
        self.draw_base(pen, dc)
        b = dc.body_bounds(offset=self.offset, width_ratio=self.width_ratio)
        # Accent dot
        draw_rect(
            pen,
            b.xmid + dc.stroke_x / 2 - self.dot_width - dc.stroke_x,
            dc.accent - self.dot_width / 2 - dc.stroke_x / 2,
            b.xmid + dc.stroke_x / 2,
            dc.accent + dc.stroke_x / 2 + self.dot_width / 2,
        )
