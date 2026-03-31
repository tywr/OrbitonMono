from config import FontConfig as fc
from glyph import Glyph
from shapes.superellipse_loop import draw_superellipse_loop


class OGlyph(Glyph):
    name = "o"
    unicode = "0x6F"

    def draw(
        self,
        pen,
        stroke: int,
    ):
        offset = 0
        width = 320
        hx = 200
        hy = 230

        x1 = fc.width / 2 - width / 2 - stroke / 2 + offset
        y1 = -fc.overshoot
        x2 = fc.width / 2 + width / 2 + stroke / 2 + offset
        y2 = fc.x_height + fc.overshoot
        draw_superellipse_loop(pen, stroke, x1, y1, x2, y2, hx, hy)
