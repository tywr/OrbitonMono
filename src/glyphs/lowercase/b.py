from config import FontConfig as fc
from glyph import Glyph
from shapes.superellipse_arch import draw_superellipse_arch
from shapes.rect import draw_rect


class LowercaseBGlyph(Glyph):
    name = "lowercase_b"
    unicode = "0x62"
    offset = 26

    def draw(
        self,
        pen,
        dc,
    ):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_right=True,
        )
        draw_superellipse_arch(
            pen,
            dc.stroke,
            b.x1,
            b.y1,
            b.x2,
            b.y2,
            dc.hx,
            dc.hy,
            dent=dc.dent + dc.v_overshoot,
            side="left",
        )
        draw_rect(pen, b.x1, 0, b.x1 + dc.stroke - dc.gap, dc.ascent)
        draw_rect(pen, b.x1, dc.dent, b.x1 + dc.stroke, dc.x_height - dc.dent)
