from config import FontConfig as fc
from glyph import Glyph
from shapes.corner import draw_corner
from shapes.rect import draw_rect


class LowercaseFGlyph(Glyph):
    name = "f"
    unicode = "0x66"

    def draw(
        self,
        pen,
        stroke: int,
    ):
        offset = -28
        len_left = 120
        len_right = 180
        corner_width = 150
        hx = 150
        hy = 150

        xmid = fc.width / 2 + offset
        # Stem
        draw_rect(pen, xmid - stroke / 2, 0, xmid + stroke / 2, fc.x_height)
        # Cross-bar
        draw_rect(
            pen,
            xmid - len_left - stroke / 2,
            fc.x_height - stroke,
            xmid + len_right + stroke / 2,
            fc.x_height,
        )
        # Corner
        draw_corner(
            pen,
            stroke,
            xmid - stroke / 2,
            fc.x_height,
            xmid + corner_width,
            fc.ascent,
            hx,
            hy,
            orientation="top-right",
        )
        # Extension after the corner to the right
        if len_right > corner_width:
            draw_rect(
                pen,
                xmid + corner_width,
                fc.ascent - stroke,
                xmid + len_right + stroke / 2,
                fc.ascent,
            )
