from config import FontConfig as fc
from glyph import Glyph
from shapes.superellipse_arch import draw_superellipse_arch
from shapes.rect import draw_rect


class LowercaseRGlyph(Glyph):
    name = "r"
    unicode = "0x72"

    def draw(
        self,
        pen,
        stroke: int,
    ):
        offset = 20
        width = fc.body_width + fc.h_overshoot
        ratio = fc.a_ratio
        hx = fc.a_hx
        hy = fc.a_hy

        x1 = fc.width / 2 - width / 2 - stroke / 2 + offset
        y1 = -fc.overshoot + ratio * fc.x_height - stroke / 2
        x2 = fc.width / 2 + width / 2 + stroke / 2 + offset
        y2 = fc.x_height + fc.overshoot

        # Arch
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
        # Ascender
        draw_rect(pen, x1, 0, x1 + stroke - fc.gap, fc.x_height)
        draw_rect(pen, x1, 0, x1 + stroke, fc.x_height - fc.tooth)
