from glyphs import Glyph
from draw.rect import draw_rect
from draw.square_corner import draw_square_corner


class LowercaseLGlyph(Glyph):
    name = "lowercase_l"
    unicode = "0x6C"
    offset = -6
    width_ratio = 1.1
    mid_ratio = 0.48

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="ascent", width_ratio=self.width_ratio
        )
        ym4 = b.y1 + b.height / 4
        xmid = b.x1 + self.mid_ratio * b.width

        # Stem
        draw_rect(pen, xmid - dc.stroke_x / 2, ym4, xmid + dc.stroke_x / 2, dc.ascent)

        # Footer
        draw_square_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            xmid - dc.stroke_x / 2,
            ym4,
            b.x2,
            b.y1,
            orientation="bottom-right",
        )

        # Left cap
        draw_rect(
            pen,
            b.x1,
            dc.ascent - dc.stroke_y,
            xmid,
            dc.ascent,
        )
