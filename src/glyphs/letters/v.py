from math import atan, cos, sin
from config import FontConfig as fc
from glyph import Glyph
from shapes.polygon import draw_polygon


class LowercaseVGlyph(Glyph):
    name = "v"
    unicode = "0x76"

    def draw(
        self,
        pen,
        stroke: int,
    ):
        offset = 0
        width = 345
        taper = 0.6

        xmid = fc.width / 2 + offset

        a = width / 2
        b = fc.x_height
        theta = atan(b / a)
        x_delta = stroke / sin(theta)
        y_delta = stroke / cos(theta)

        draw_polygon(
            pen,
            points=[
                (xmid + taper * x_delta / 2, 0),
                (xmid + width / 2 + x_delta / 2, fc.x_height),
                (xmid + width / 2 - x_delta / 2, fc.x_height),
                (xmid, taper * y_delta),
                (xmid - width / 2 + x_delta / 2, fc.x_height),
                (xmid - width / 2 - x_delta / 2, fc.x_height),
                (xmid - taper * x_delta / 2, 0),
            ],
        )
