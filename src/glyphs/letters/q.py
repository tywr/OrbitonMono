from config import FontConfig as fc
from glyph import Glyph
from shapes.superellipse_arch import draw_superellipse_arch
from shapes.rect import draw_rect


class LowercaseQGlyph(Glyph):
    name = "q"
    unicode = "0x71"

    def draw(
        self,
        pen,
        stroke: int,
    ):
        offset = 0
        width = fc.body_width + fc.h_overshoot
        hx = fc.hx
        hy = fc.hy

        x1 = fc.width / 2 - width / 2 - stroke / 2 + offset
        y1 = -fc.overshoot
        x2 = fc.width / 2 + width / 2 + stroke / 2 + offset
        y2 = fc.x_height + fc.overshoot

        # Right-ear
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
        )
        # Descender
        draw_rect(pen, x2 - stroke + fc.gap, fc.descent, x2, fc.x_height)
        draw_rect(pen, x2 - stroke, fc.tooth, x2, fc.x_height - fc.tooth)
