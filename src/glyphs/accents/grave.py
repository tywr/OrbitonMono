from glyphs.accents import Accent
from draw.parallelogramm import draw_parallelogramm_vertical


class Grave(Accent):
    name = "grave"
    unicode = "0x60"
    height = 0.4
    width = 1

    def draw_at(self, pen, dc, x, y):
        h = self.height * dc.x_height
        w = self.width * dc.width
        draw_parallelogramm_vertical(
            pen,
            dc.stroke_alt,
            dc.stroke_alt,
            x + w / 2,
            y - h / 2,
            x - w / 2,
            y + h / 2,
        )
