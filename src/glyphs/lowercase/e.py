from glyphs import Glyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.corner import draw_corner
from draw.rect import draw_rect


class LowercaseEGlyph(Glyph):
    name = "lowercase_e"
    unicode = "0x65"
    offset = 0
    width_ratio = 1

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_left=True,
            overshoot_right=True,
            width_ratio=self.width_ratio,
        )

        # Half-top of a superellipse
        draw_superellipse_loop(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1,
            b.x2,
            b.y2,
            b.hx,
            b.hy,
            cut="bottom",
        )

        # Corner from mid-left to bottom
        draw_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.ymid + 2 * dc.v_overshoot,
            b.xmid,
            0,
            dc.hx,
            dc.hy,
            orientation="bottom-right",
        )
        # Extension
        draw_rect(pen, b.xmid, 0, b.x2 - dc.stroke_x / 2, dc.stroke_y)

        # Mid-bar
        draw_rect(
            pen,
            b.x1 + dc.stroke_x / 2,
            b.ymid,
            b.x2 - dc.stroke_x / 2,
            b.ymid + dc.stroke_alt / 2,
        )
        draw_rect(pen, b.x1 + dc.stroke_x / 2, b.ymid - dc.stroke_alt / 2, b.x2, b.ymid)
