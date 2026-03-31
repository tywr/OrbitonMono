from config import FontConfig as fc
from glyph import Glyph
from shapes.corner import draw_corner
from shapes.rect import draw_rect


class LowercaseTGlyph(Glyph):
    name = "t"
    unicode = "0x74"

    def draw(
        self,
        pen,
        stroke: int,
    ):
        offset = -50
        len_left = 120
        len_right = 190
        corner_width = 180
        corner_height = 250
        hx = 180
        hy = 240

        xmid = fc.width / 2 + offset

        # Stem
        draw_rect(pen, xmid - stroke / 2, corner_height, xmid + stroke / 2, fc.ascent)
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
            corner_height,
            xmid + corner_width,
            0,
            hx,
            hy,
            orientation="bottom-right",
        )
        # Extension after the corner to the right
        if len_right > corner_width:
            draw_rect(
                pen,
                xmid + corner_width,
                0,
                xmid + len_right + stroke / 2,
                stroke,
            )
