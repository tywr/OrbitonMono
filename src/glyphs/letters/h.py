from config import FontConfig as fc
from glyph import Glyph
from shapes.superellipse_arch import draw_superellipse_arch
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
        hx = 135
        hy = 150
        loop_ratio = 0.6

        x1 = fc.width / 2 - width / 2 - stroke / 2 + offset
        y1 = fc.x_height - (fc.x_height + fc.overshoot) * loop_ratio
        x2 = fc.width / 2 + width / 2 + stroke / 2 + offset
        y2 = fc.x_height + fc.overshoot
        draw_superellipse_arch(
            pen,
            stroke,
            x1,
            y1,
            x2,
            y2,
            hx,
            hy,
            tooth=fc.tooth + fc.overshoot,
            side="left",
            cut="bottom",
        )
        # Left stem
        draw_rect(pen, x1, 0, x1 + stroke, fc.x_height - fc.tooth)
        draw_rect(pen, x1, 0, x1 + stroke - fc.gap, fc.ascent)
        # Right stem
        draw_rect(
            pen,
            x2 - stroke,
            0,
            x2,
            fc.x_height
            - ((fc.x_height + fc.overshoot) * loop_ratio + fc.overshoot) / 2
            + fc.overshoot,
        )
