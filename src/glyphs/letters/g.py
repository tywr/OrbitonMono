from config import FontConfig as fc
from glyph import Glyph
from shapes.superellipse_arch import draw_superellipse_arch
from shapes.rect import draw_rect
from shapes.corner import draw_corner


class LowercaseGGlyph(Glyph):
    name = "g"
    unicode = "0x67"

    def draw(
        self,
        pen,
        stroke: int,
    ):
        offset = 15
        width = fc.body_width + fc.h_overshoot
        hx = fc.hx
        hy = fc.hy
        corner_width = 160
        corner_hx = 100
        corner_hy = 115

        x1 = fc.width / 2 - width / 2 - stroke / 2 + offset
        y1 = -fc.overshoot
        x2 = fc.width / 2 + width / 2 + stroke / 2 + offset
        y2 = fc.x_height + fc.overshoot
        # Bowl
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
        # Right step
        draw_rect(pen, x2 - stroke + fc.gap, 0, x2, fc.x_height)
        draw_rect(pen, x2 - stroke, fc.tooth, x2, fc.x_height - fc.tooth)
        # Curve to the bottom left
        draw_corner(
            pen,
            stroke - fc.gap,
            x2,
            0,
            x2 - corner_width,
            fc.descent + fc.tail_offset,
            corner_hx,
            corner_hy,
            orientation="bottom-left",
        )
        draw_rect(
            pen,
            x1 + stroke / 2,
            fc.descent + fc.tail_offset,
            x2 - corner_width,
            fc.descent + fc.tail_offset + stroke - fc.gap,
        )
