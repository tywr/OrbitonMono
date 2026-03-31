from math import atan, cos
from config import FontConfig as fc
from glyph import Glyph
from shapes.rect import draw_rect
from shapes.polygon import draw_polygon


class LowercaseZGlyph(Glyph):
    name = "z"
    unicode = "0x78"

    def draw(
        self,
        pen,
        stroke: int,
    ):
        offset = 0
        width = 320

        x1 = fc.width / 2 - width / 2 - stroke / 2 + offset
        y1 = 0
        x2 = fc.width / 2 + width / 2 + stroke / 2 + offset
        y2 = fc.x_height

        theta = atan((y2 - y1 - 2 * stroke) / (x2 - x1))
        delta = stroke / cos(theta)

        draw_rect(pen, x1, fc.x_height - stroke, x2, fc.x_height)
        draw_rect(pen, x1, 0, x2, stroke)
        draw_polygon(
            pen,
            points=[
                (x1, y1 + stroke),
                (x1 + delta, y1 + stroke),
                (x2, y2 - stroke),
                (x2 - delta, y2 - stroke),
            ],
        )
