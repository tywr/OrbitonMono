from config import FontConfig as fc
from glyph import Glyph
from shapes.superellipse_loop import draw_superellipse_loop
from shapes.corner import draw_corner
from shapes.rect import draw_rect


class LowercaseEGlyph(Glyph):
    name = "e"
    unicode = "0x65"

    def draw(
        self,
        pen,
        stroke: int,
    ):
        offset = 15
        width = fc.body_width + 2 * fc.h_overshoot
        hx = fc.hx
        hy = fc.hy

        x1 = fc.width / 2 - width / 2 - stroke / 2 + offset
        y1 = -fc.overshoot
        x2 = fc.width / 2 + width / 2 + stroke / 2 + offset
        y2 = fc.x_height + fc.overshoot
        ymid = y1 + (y2 - y1) / 2
        xmid = x1 + (x2 - x1) / 2

        # Half-top of a superellipse
        draw_superellipse_loop(pen, stroke, x1, y1, x2, y2, hx, hy, cut="bottom")
        # Corner from mid-left to bottom
        draw_corner(
            pen,
            stroke,
            x1,
            (fc.x_height + 2 * fc.overshoot) / 2 + fc.overshoot,
            xmid,
            0,
            hx,
            hy,
            orientation="bottom-right",
        )
        # Extension
        draw_rect(pen, xmid, 0, x2 - stroke / 2, stroke)
        # Mid-bar
        draw_rect(pen, x1 + stroke / 2, ymid, x2 - stroke / 2, ymid + stroke / 2)
        draw_rect(pen, x1 + stroke / 2, ymid - stroke / 2, x2, ymid)
