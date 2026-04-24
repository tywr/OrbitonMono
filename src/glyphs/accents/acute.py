from glyphs.accents import Accent
from draw.parallelogramm import draw_parallelogramm


class Acute(Accent):
    name = "acute"
    unicode = "0xB4"
    height = 0.35
    width = 0.65
    stroke_ratio = 1.2

    def draw_at(self, pen, dc, x, y):
        h = self.height * dc.x_height
        w = self.width * dc.width
        d = self.stroke_ratio * dc.stroke_x
        draw_parallelogramm(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            x - d / 2,
            y - h / 2,
            x + w - d / 2,
            y + h / 2,
            delta=d,
        )
