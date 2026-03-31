from config import FontConfig as fc
from glyph import Glyph
from shapes.rect import draw_rect


class LowercaseLGlyph(Glyph):
    name = "l"
    unicode = "0x6C"

    def draw(
        self,
        pen,
        stroke: int,
    ):
        offset = 20
        len_left = 150
        len_right = 160
        len_cap = 140

        xmid = fc.width / 2 + offset
        # Stem
        draw_rect(pen, xmid - stroke / 2, 0, xmid + stroke / 2, fc.ascent)
        # Footer
        draw_rect(
            pen,
            xmid - len_left - stroke / 2,
            0,
            xmid + len_right + stroke / 2,
            stroke,
        )
        # Left cap
        draw_rect(
            pen,
            xmid - len_cap - stroke / 2,
            fc.ascent - stroke,
            xmid,
            fc.ascent,
        )
