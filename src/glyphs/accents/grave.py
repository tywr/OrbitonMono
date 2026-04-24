from glyphs.accents import Accent
from draw.parallelogramm import draw_parallelogramm


class Grave(Accent):
    name = "grave"
    unicode = "0x60"
    height = 0.35
    width = 0.65
    stroke_ratio = 1.2

    def draw_at(self, pen, dc, x, y):
        h = self.height * dc.x_height
        w = self.width * dc.width
        d = self.stroke_ratio * dc.stroke_x
        draw_parallelogramm(
            pen,
            dc.stroke_alt,
            dc.stroke_alt,
            x + d / 2,
            y - h / 2,
            x + d / 2 - w,
            y + h / 2,
            delta=d,
            direction="top-left"
        )
