from glyphs import Glyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.corner import draw_corner
from draw.smooth_corner import draw_smooth_corner
from draw.rect import draw_rect


class LowercaseEGlyph(Glyph):
    name = "lowercase_e"
    unicode = "0x65"
    offset = 0
    width_ratio = 1
    stroke_x_ratio = 1.00
    stroke_y_ratio = 0.96

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_top=True,
            overshoot_left=True,
            width_ratio=self.width_ratio,
        )
        sx, sy = self.stroke_x_ratio * dc.stroke_x, self.stroke_y_ratio * dc.stroke_y

        # Half-top of a superellipse
        draw_superellipse_loop(
            pen,
            sx,
            sy,
            b.x1,
            b.y1,
            b.x2,
            b.y2,
            b.hx,
            b.hy,
            cut="bottom",
        )

        # Corner from mid-left to bottom
        draw_smooth_corner(
            pen,
            sx,
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
        draw_rect(pen, b.xmid, 0, b.x2 - 0.33 * dc.stroke_x, dc.stroke_y)

        # Mid-bar
        draw_rect(
            pen,
            b.x1 + 0.75 * dc.stroke_x,
            b.ymid,
            b.x2 - dc.stroke_x / 2,
            b.ymid + dc.stroke_alt / 2,
        )
        draw_rect(
            pen, b.x1 + 0.75 * dc.stroke_x, b.ymid - dc.stroke_alt / 2, b.x2, b.ymid
        )
