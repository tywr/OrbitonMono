from glyphs import Glyph
from draw.s_curve import draw_s_curve
from draw.corner import draw_corner
from draw.parallelogramm import draw_smooth_parallelogramm_vertical


class LowercaseSGlyph(Glyph):
    name = "lowercase_s"
    unicode = "0x73"
    offset = 0
    width_ratio = 1
    stroke_x_ratio = 1.00
    left_tail_offset = 0.02
    right_tail_offset = 0.015
    hx_ratio = 0.75
    hy_ratio = 0.8
    top_height_ratio = 0.28
    bottom_height_ratio = 0.29
    tail_dip = 0.007
    tail_offset = 0.08
    hy_curve_ratio = 1.2

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            width_ratio=self.width_ratio,
        )
        sx, sy = self.stroke_x_ratio * dc.stroke_x, dc.stroke_y
        hx, hy = b.hx * self.hx_ratio, b.hy * self.hy_ratio
        xl = b.x1 + self.left_tail_offset * b.width
        xr = b.x2 - self.right_tail_offset * b.width

        xt_top = b.x2 - self.tail_offset * b.width
        yt_top = dc.x_height - self.tail_dip * b.height - sy
        xt_bot = b.x1 + self.tail_offset * b.width
        yt_bot = sy

        ltop = self.top_height_ratio * b.height
        lbot = self.bottom_height_ratio * b.height
        yr, yl = b.y1 + lbot, b.y2 - ltop

        draw_corner(pen, sx, sy, xl, yl, b.xmid, b.y2, hx, hy, orientation="top-right")
        draw_corner(
            pen, sx, sy, xr, yr, b.xmid, b.y1, hx, hy, orientation="bottom-left"
        )

        draw_smooth_parallelogramm_vertical(
            pen, sy, b.xmid, b.y2, xt_top, yt_top, direction="bottom-right"
        )
        draw_smooth_parallelogramm_vertical(
            pen,
            sy,
            b.xmid,
            b.y1,
            xt_bot,
            yt_bot,
            direction="top-left",
        )

        draw_s_curve(
            pen,
            sx,
            sy,
            xl,
            yr,
            xr,
            yl,
            hx,
            hy * self.hy_curve_ratio,
            middle_y_ratio=0.52,
            dx=112,
            dy=112,
        )
