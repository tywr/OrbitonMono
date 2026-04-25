from glyphs.accents import Accent
from draw.parallelogramm import draw_parallelogramm


class Caron(Accent):
    name = "caron"
    unicode = "0x2C7"
    height = 0.35
    width = 1.3
    stroke_ratio = 1.2

    def draw_at(self, pen, dc, x, y):
        h = self.height * dc.x_height
        w = self.width * dc.width
        x1, x2, xmid = x - w / 2, x + w / 2, x
        y1, y2 = y - h / 2, y + h / 2
        d = self.stroke_ratio * dc.stroke_x
        ov = 0.5 * d

        draw_parallelogramm(
            pen,
            dc.stroke_alt,
            dc.stroke_alt,
            xmid + ov,
            y1,
            x1,
            y2,
            direction="top-left",
            delta=d,
        )
        draw_parallelogramm(
            pen,
            dc.stroke_alt,
            dc.stroke_alt,
            xmid - ov,
            y1,
            x2,
            y2,
            direction="top-right",
            delta=d,
        )
