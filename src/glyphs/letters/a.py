from config import FontConfig as fc
from glyph import Glyph
from shapes.superellipse_ear import draw_superellipse_ear
from shapes.corner import draw_corner
from shapes.rect import draw_rect


class LowercaseAGlyph(Glyph):
    name = "a"
    unicode = "0x61"

    def draw(
        self,
        pen,
        stroke: int,
    ):
        offset = 0
        width = fc.body_width + fc.h_overshoot
        loop_ratio = 0.6
        hx = 135
        hy = 150
        cap_hx = 180
        cap_hy = 160
        len_cap = 225

        x1 = fc.width / 2 - width / 2 - stroke / 2 + offset
        y1 = -fc.overshoot
        x2 = fc.width / 2 + width / 2 + stroke / 2 + offset
        y2 = loop_ratio * (fc.x_height + fc.overshoot)
        xmid = x1 + (x2 - x1) / 2

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
            side="right",
            cut="top",
        )
        draw_rect(pen, x2 - stroke, 0, x2, fc.x_height / 2)
        # Curve to the cap
        draw_corner(
            pen,
            stroke,
            x2,
            fc.x_height / 2,
            xmid,
            fc.x_height,
            cap_hx,
            cap_hy,
            orientation="top-left",
        )
        # Cap
        draw_rect(pen, xmid - len_cap / 2 - stroke / 2, fc.x_height - stroke, xmid, fc.x_height)
        draw_corner(
            pen,
            stroke,
            x1,
            loop_ratio * (fc.x_height + 2 * fc.overshoot) / 2 - fc.overshoot,
            xmid,
            loop_ratio * fc.x_height,
            hx,
            hy,
            orientation="top-right",
        )
        draw_rect(
            pen,
            xmid,
            fc.x_height * loop_ratio - stroke,
            x2 - stroke,
            fc.x_height * loop_ratio,
        )
