from config import FontConfig as fc
from glyph import Glyph
from shapes.corner import draw_corner
from shapes.rect import draw_rect


class LowercaseJGlyph(Glyph):
    name = "j"
    unicode = "0x6A"

    def draw(
        self,
        pen,
        stroke: int,
    ):
        offset = 54
        len_left = 200
        corner_width = 160
        hx = 160
        hy = 160
        dot_width = 23
        len_cap = 140

        xmid = fc.width / 2 + offset
        # Stem
        draw_rect(pen, xmid - stroke / 2, 0, xmid + stroke / 2, fc.x_height)
        # Left cap
        draw_rect(
            pen,
            xmid - len_cap - stroke / 2,
            fc.x_height - stroke,
            xmid,
            fc.x_height,
        )
        # Bottom left corner part
        draw_corner(
            pen,
            stroke,
            xmid + stroke / 2,
            0,
            xmid - corner_width,
            fc.descent + fc.tail_offset,
            hx,
            hy,
            orientation="bottom-left",
        )
        # Extension after the corner to the left
        if len_left > corner_width:
            draw_rect(
                pen,
                xmid - len_left - stroke / 2,
                fc.descent + fc.tail_offset,
                xmid - corner_width,
                fc.descent + fc.tail_offset + stroke,
            )
        # Accent dot
        draw_rect(
            pen,
            xmid - dot_width - stroke / 2,
            fc.accent - dot_width / 2 - stroke / 2,
            xmid + stroke / 2,
            fc.accent + stroke / 2 + dot_width / 2,
        )
