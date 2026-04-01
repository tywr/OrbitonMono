from math import atan, cos, sin
from config import FontConfig as fc
from glyph import Glyph
from shapes.polygon import draw_polygon


class LowercaseWGlyph(Glyph):
    name = "w"
    unicode = "0x77"

    def draw(
        self,
        pen,
        stroke: int,
    ):
        offset = 0
        width = 400
        overlap = 40
        taper = 0.6
        joint_height = 0.8 * fc.x_height

        xmid = fc.width / 2 + offset
        xmid1 = fc.width / 4 + offset + overlap
        xmid2 = 3 * fc.width / 4 + offset - overlap

        a = width / 4
        b = fc.x_height / 2
        theta = atan(b / a)

        x_delta = stroke / sin(theta)
        y_delta = stroke / cos(theta)

        draw_polygon(
            pen,
            points=[
                (xmid1 + taper * x_delta / 2, 0),
                (xmid + taper * x_delta / 2, joint_height),
                (xmid - taper * x_delta / 2, joint_height),
                (xmid1, taper * y_delta),
                (xmid1 - width / 4 + x_delta / 2, fc.x_height),
                (xmid1 - width / 4 - x_delta / 2, fc.x_height),
                (xmid1 - x_delta / 2, 0),
            ],
        )
        draw_polygon(
            pen,
            points=[
                (xmid2 + x_delta / 2, 0),
                (xmid2 + width / 4 + x_delta / 2, fc.x_height),
                (xmid2 + width / 4 - x_delta / 2, fc.x_height),
                (xmid2, taper * y_delta),
                (xmid + taper * x_delta / 2, joint_height),
                (xmid - taper * x_delta / 2, joint_height),
                (xmid2 - taper * x_delta / 2, 0),
            ],
        )
