from config import FontConfig as fc
from glyph import Glyph
from shapes.superellipse_arch import draw_superellipse_arch
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
        hx = 120
        hy = fc.hy
        mid_len = 0.6

        x1 = fc.width / 2 - width / 2 - stroke / 2 + offset
        y1 = -fc.overshoot
        x2 = fc.width / 2 + width / 2 + stroke / 2 + offset
        y2 = fc.x_height + fc.overshoot
        xmid = x1 + (x2 - x1) / 2

        # Left arch
        draw_superellipse_arch(
            pen,
            stroke,
            x1,
            y1,
            xmid + stroke / 2,
            y2,
            hx,
            hy,
            tooth=fc.tooth + fc.overshoot,
            side="left",
            cut="bottom",
        )
        # Right arch
        draw_superellipse_arch(
            pen,
            stroke,
            xmid - stroke / 2,
            y1,
            x2,
            y2,
            hx,
            hy,
            tooth=fc.tooth + fc.overshoot,
            side="left",
            cut="bottom",
        )
        # Left foot
        draw_rect(pen, x1, 0, x1 + stroke, fc.x_height)
        # Right foot
        draw_rect(
            pen, x2 - stroke, 0, x2, (fc.x_height + 2 * fc.overshoot) / 2 - fc.overshoot
        )
        # Middle extension
        draw_rect(
            pen,
            xmid - stroke / 2,
            200,
            xmid + stroke / 2,
            fc.x_height - fc.tooth,
        )
