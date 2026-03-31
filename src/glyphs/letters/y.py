from math import atan, cos, sin
from config import FontConfig as fc
from glyph import Glyph
from shapes.polygon import draw_polygon


class LowercaseYGlyph(Glyph):
    name = "y"
    unicode = "0x77"

    def draw(
        self,
        pen,
        stroke: int,
    ):
        offset = 0
        width = 345
        dent_height = 40

        xmid = fc.width / 2 + offset

        a = width / 2
        b = fc.x_height / 2
        theta = atan(b / a)
        x_delta = stroke / sin(theta)
        y_delta = stroke / cos(theta)

        x_delta_desc = -fc.descent * (width / 2) / fc.x_height

        x_delta_dent = dent_height * (width / 2) / fc.x_height

        draw_polygon(
            pen,
            points=[
                # Starting from left side of the tail
                (xmid - x_delta / 2 - x_delta_desc, fc.descent),
                (xmid + x_delta / 2 - x_delta_desc, fc.descent),
                # Top-right
                (xmid + width / 2 + x_delta / 2, fc.x_height),
                (xmid + width / 2 - x_delta / 2, fc.x_height),
                # Inner middle-part
                (xmid, y_delta),
                # Top-left
                (xmid - width / 2 + x_delta / 2, fc.x_height),
                (xmid - width / 2 - x_delta / 2, fc.x_height),
                # Dent
                (xmid - x_delta / 2 - x_delta_dent, dent_height),
                (xmid - x_delta / 2 + x_delta_dent, dent_height),
            ],
        )
