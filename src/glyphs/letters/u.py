from config import FontConfig as fc
from glyph import Glyph
from shapes.superellipse_arch import draw_superellipse_arch
from shapes.rect import draw_rect


class LowercaseUGlyph(Glyph):
    name = "u"
    unicode = "0x75"

    def draw(
        self,
        pen,
        stroke: int,
    ):
        offset = 0
        width = fc.body_width
        hx = 135
        hy = 150
        loop_ratio = 0.6

        x1 = fc.width / 2 - width / 2 - stroke / 2 + offset
        y1 = -fc.overshoot
        x2 = fc.width / 2 + width / 2 + stroke / 2 + offset
        y2 = loop_ratio * (fc.x_height + fc.overshoot)
        # Shoulder
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
            side="right",
            cut="top",
        )
        # Right ascent
        draw_rect(pen, x2 - stroke, fc.tooth, x2, fc.x_height)
        draw_rect(pen, x2 - stroke + fc.gap, 0, x2, fc.x_height)
        # Left ascent
        draw_rect(
            pen,
            x1,
            ((fc.x_height + fc.overshoot) * loop_ratio + fc.overshoot) / 2
            - fc.overshoot,
            x1 + stroke,
            fc.x_height,
        )
