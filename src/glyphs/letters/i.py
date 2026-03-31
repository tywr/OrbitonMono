from config import FontConfig as fc
from glyph import Glyph
from shapes.rect import draw_rect


class LowercaseIGlyph(Glyph):
    name = "i"
    unicode = "0x69"

    def draw(
        self,
        pen,
        stroke: int,
    ):
        offset = 30
        len_left = 150
        len_right = 160
        dot_width = 43
        len_cap = 140

        xmid = fc.width / 2 + offset
        # Stem
        draw_rect(pen, xmid - stroke / 2, 0, xmid + stroke / 2, fc.x_height)
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
            fc.x_height - stroke,
            xmid,
            fc.x_height,
        )
        # Accent dot
        draw_rect(
            pen,
            xmid - dot_width - stroke / 2,
            fc.accent - dot_width / 2 - stroke / 2,
            xmid + stroke / 2,
            fc.accent + stroke / 2 + dot_width / 2,
        )
