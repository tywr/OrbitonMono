from math import sqrt
from glyphs.accents import Accent


K_CIRCLE = 4 * (sqrt(2) - 1) / 3


def _draw_circle(pen, cx, cy, r, clockwise=False):
    k = K_CIRCLE * r
    pen.moveTo((cx + r, cy))
    if clockwise:
        pen.curveTo((cx + r, cy - k), (cx + k, cy - r), (cx, cy - r))
        pen.curveTo((cx - k, cy - r), (cx - r, cy - k), (cx - r, cy))
        pen.curveTo((cx - r, cy + k), (cx - k, cy + r), (cx, cy + r))
        pen.curveTo((cx + k, cy + r), (cx + r, cy + k), (cx + r, cy))
    else:
        pen.curveTo((cx + r, cy + k), (cx + k, cy + r), (cx, cy + r))
        pen.curveTo((cx - k, cy + r), (cx - r, cy + k), (cx - r, cy))
        pen.curveTo((cx - r, cy - k), (cx - k, cy - r), (cx, cy - r))
        pen.curveTo((cx + k, cy - r), (cx + r, cy - k), (cx + r, cy))
    pen.closePath()


class Ring(Accent):
    name = "ring"
    unicode = "0x2DA"
    width = 0.6
    stroke_ratio = 0.8

    def draw_at(self, pen, dc, x, y):
        stroke = dc.stroke_alt * self.stroke_ratio
        r_outer = dc.width * self.width / 2
        r_inner = r_outer - stroke
        _draw_circle(pen, x, y, r_outer, clockwise=False)
        _draw_circle(pen, x, y, r_inner, clockwise=True)
