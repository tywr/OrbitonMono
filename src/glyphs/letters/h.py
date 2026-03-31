from config import FontConfig as fc
from glyph import Glyph
from shapes.superellipse_ear import draw_superellipse_ear
from shapes.rect import draw_rect


class LowercaseHGlyph(Glyph):
    name = "h"
    unicode = "0x68"

    def draw(
        self,
        pen,
        stroke: int,
    ):
        offset = 24
        width = fc.body_width
        hx = fc.hx
        hy = fc.hy

        x1 = fc.width / 2 - width / 2 - stroke / 2 + offset
        y1 = -fc.overshoot
        x2 = fc.width / 2 + width / 2 + stroke / 2 + offset
        y2 = fc.x_height + fc.overshoot
        draw_superellipse_ear(
            pen,
            stroke,
            x1,
            y1,
            x2,
            y2,
            hx,
            hy,
            fc.tooth,
            fc.cover,
            side="left",
            cut="bottom",
        )
        draw_rect(pen, x1, 0, x1 + stroke, fc.ascent)
        draw_rect(pen, x2 - stroke, 0, x2, (fc.x_height + 2 * fc.overshoot) / 2 - fc.overshoot)
