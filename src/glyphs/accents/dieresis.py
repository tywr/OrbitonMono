from glyphs.accents import Accent
from draw.rect import draw_rect


class Dieresis(Accent):
    name = "dieresis"
    unicode = "0xA8"
    gap = 0.38
    stroke_width = 1.1

    def draw_at(self, pen, dc, x, y):
        dw = self.stroke_width * dc.stroke_x / 2
        g = self.gap * dc.width
        xm1 = x - g / 2 - dw / 2
        xm2 = x + g / 2 + dw / 2

        # Left dot
        draw_rect(pen, xm1 - dw, y - dw, xm1 + dw, y + dw)
        draw_rect(pen, xm2 - dw, y - dw, xm2 + dw, y + dw)
