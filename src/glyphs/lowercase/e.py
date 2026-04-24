from glyphs import Glyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.corner import draw_corner
from draw.rect import draw_rect
from draw.parallelogramm import draw_parallelogramm_vertical


class LowercaseEGlyph(Glyph):
    name = "lowercase_e"
    unicode = "0x65"
    offset = 5
    width_ratio = 1
    stroke_x_ratio = 1.00
    stroke_y_ratio = 0.96
    mid_height = 0.5
    thinning = 0.5
    stroke_x_ratio = 1.04
    stroke_y_ratio = 0.96
    overshoot_reducing = 0.65
    tail_offset = 0.08

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_top=True,
            overshoot_bottom=True,
            overshoot_left=True,
            overshoot_right=True,
            width_ratio=self.width_ratio,
        )
        sx, sy = self.stroke_x_ratio * dc.stroke_x, self.stroke_y_ratio * dc.stroke_y
        hx, hy = b.hx * (b.width - dc.h_overshoot) / b.width, b.hy
        ymid = self.mid_height * b.height
        yt = sy + dc.v_overshoot
        xt = b.x2 - self.tail_offset * b.width

        # Half-top of a superellipse
        draw_superellipse_loop(
            pen,
            sx,
            sy,
            b.x1,
            # b.y1 + self.overshoot_reducing * dc.v_overshoot,
            b.y1,
            b.x2,
            b.y2,
            b.hx,
            b.hy,
            cut="right",
        )

        draw_corner(
            pen,
            sx,
            sy,
            b.x2 - dc.h_overshoot,
            ymid,
            b.xmid,
            b.y2,
            hx,
            hy,
            orientation="top-left",
        )

        # Tail of e
        draw_parallelogramm_vertical(
            pen, sx, sy, b.xmid, b.y1, xt, yt, direction="top-right", delta=sy
        )

        # Middle bar
        draw_rect(
            pen,
            b.x1 + sx / 2,
            ymid,
            b.x2 - dc.h_overshoot - sx / 2,
            ymid + dc.stroke_alt / 2,
        )
        draw_rect(
            pen, b.x1 + sx / 2, ymid - dc.stroke_alt / 2, b.x2 - dc.h_overshoot, ymid
        )
