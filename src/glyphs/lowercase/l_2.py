from glyphs import Glyph
from draw.rect import draw_rect
from draw.corner import draw_corner


class LowercaseL2Glyph(Glyph):
    name = "lowercase_l_2"
    unicode = "0x6C"
    font_feature = {"ss03": 1}
    default_italic = True
    offset = 4
    width_ratio = 1.08
    cap = 0.5

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="ascent", width_ratio=self.width_ratio
        )
        right_len = 0.5 * b.width - dc.stroke_x / 2
        left_len = 0.5 * b.width - dc.stroke_x / 2
        ym4 = b.y1 + b.height / 4

        # Stem
        draw_rect(pen, b.xmid - dc.stroke_x / 2, ym4, b.xmid + dc.stroke_x / 2, dc.ascent)

        # Footer
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

        # Left cap
        draw_rect(
            pen,
            b.xmid - b.width * self.cap,
            dc.ascent - dc.stroke_y,
            b.xmid,
            dc.ascent,
        )
