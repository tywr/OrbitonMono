from config import FontConfig as fc
from glyph import Glyph
from shapes.superellipse_ear import draw_superellipse_ear
from shapes.rect import draw_rect


class LowercaseMGlyph(Glyph):
    name = "m"
    unicode = "0x6D"

    def draw(
        self,
        pen,
        stroke: int,
    ):
        offset = 0
        width = 400
        hx = 160
        hy = 160
        mid_len = 0.6

        x1 = fc.width / 2 - width / 2 - stroke / 2 + offset
        y1 = -fc.overshoot
        x2 = fc.width / 2 + width / 2 + stroke / 2 + offset
        y2 = fc.x_height + fc.overshoot
        xmid = x1 + (x2 - x1) / 2

        # Left ear
        draw_superellipse_ear(
            pen,
            stroke,
            x1,
            y1,
            xmid + stroke / 2,
            y2,
            hx,
            hy,
            fc.tooth,
            fc.cover,
            side="left",
            cut="bottom",
        )
        # Right ear
        draw_superellipse_ear(
            pen,
            stroke,
            xmid - stroke,
            y1,
            x2,
            y2,
            hx,
            hy - stroke / 2,
            fc.tooth,
            fc.cover,
            side="left",
            cut="bottom",
        )
        # Left foot
        draw_rect(pen, x1, 0, x1 + stroke, fc.x_height)
        # Right foot
        draw_rect(pen, x2 - stroke, 0, x2, (fc.x_height + 2 * fc.overshoot) / 2 - fc.overshoot)
        # Middle extension
        draw_rect(pen, xmid - stroke /2, (1 - mid_len) * fc.x_height - stroke / 2, xmid + stroke / 2, fc.x_height / 2)
