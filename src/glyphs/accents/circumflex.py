from glyphs.accents import Accent
from draw.parallelogramm import draw_parallelogramm


class Circumflex(Accent):
    name = "circumflex"
    unicode = "0x5E"
    height = 0.4
    width = 1.2
    overlap = 0.5

    def draw_at(self, pen, dc, x, y):
        h = self.height * dc.x_height
        w = self.width * dc.width
        x1, x2, xmid = x - w / 2, x + w / 2, x
        y1, y2 = y - h / 2, y + h / 2
        ov = dc.stroke_x * self.overlap

        draw_parallelogramm(
            pen,
            dc.stroke_alt,
            dc.stroke_alt,
            x1,
            y1,
            xmid + ov,
            y2,
        )
        draw_parallelogramm(
            pen, dc.stroke_alt, dc.stroke_alt, x2, y1, xmid - ov, y2, direction="top-left"
        )
