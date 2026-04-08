from glyphs.accents import Accent
from draw.rect import draw_rect


class Dieresis(Accent):
    name = "dieresis"
    unicode = "0xA8"
    gap = 0.45
    dot_width = 8

    def draw_at(self, pen, dc, x, y):
        dw = dc.stroke_x / 2 + self.dot_width
        g = self.gap * dc.width
        xm1 = x - g / 2 - dw / 2
        xm2 = x + g / 2 + dw / 2

        # Left dot
        draw_rect(pen, xm1 - dw, y - dw, xm1 + dw, y + dw)
        draw_rect(pen, xm2 - dw, y - dw, xm2 + dw, y + dw)
