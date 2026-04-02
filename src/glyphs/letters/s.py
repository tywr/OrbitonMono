from config import FontConfig as fc
from glyph import Glyph
from shapes.superellipse_loop import draw_superellipse_loop
from shapes.cross_curve import draw_cross_curve


class LowercaseSGlyph(Glyph):
    name = "s"
    unicode = "0x73"

    def draw(
        self,
        pen,
        stroke: int,
    ):
        offset = 0
        width = fc.body_width + 2 * fc.h_overshoot
        ratio = fc.a_ratio
        hx = fc.a_hx
        hy = fc.a_hy

        x1 = fc.width / 2 - width / 2 - stroke / 2 + offset
        y1 = -fc.overshoot
        x2 = fc.width / 2 + width / 2 + stroke / 2 + offset
        y2 = fc.x_height + fc.overshoot
        ymid = y1 + (y2 - y1) / 2

        loop_len = (fc.x_height + fc.overshoot) * ratio
        ym1 = -fc.overshoot + loop_len - stroke / 2
        ym2 = fc.x_height + fc.overshoot - loop_len + stroke / 2
        delta_y = ratio * (fc.x_height + 2 * fc.overshoot) / 2

        # Bottom arch
        draw_superellipse_loop(
            pen,
            stroke,
            x1,
            y1,
            x2,
            ym1,
            hx,
            hy,
            cut="top",
        )
        draw_superellipse_loop(
            pen,
            stroke,
            x1,
            ym2,
            x2,
            y2,
            hx,
            hy,
            cut="bottom",
        )
        # Middle cross junction
        draw_cross_curve(
            pen,
            stroke,
            x1,
            y1 + (ym1 - y1) / 2,
            x2,
            y2 - (y2 - ym2) / 2,
            hx,
            hy,
            invert=True,
        )
