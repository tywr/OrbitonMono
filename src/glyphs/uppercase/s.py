from glyphs.uppercase import UppercaseGlyph
from draw.parallelogramm import draw_smooth_parallelogramm_vertical
from draw.superellipse_loop import draw_superellipse_loop


class UppercaseSGlyph(UppercaseGlyph):
    name = "uppercase_s"
    unicode = "0x53"
    offset = 0
    width_ratio = 1
    stroke_x_ratio = 1.00
    right_tail_offset = 0.105
    left_tail_offset = 0.0525
    hx_ratio = 1
    hy_ratio = 1.35
    mid_height = 0.53
    width_ratio = 1.06

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            width_ratio=self.width_ratio,
            height="cap",
        )
        sx, sy = self.stroke_x_ratio * dc.stroke_x, dc.stroke_y
        hx, hy = b.hx * self.hx_ratio, b.hy * self.hy_ratio

        ymid = b.y1 + self.mid_height * b.height

        xt_top = b.x2 - self.right_tail_offset * b.width
        yt_top = dc.cap - sy - dc.v_overshoot
        xt_bot = b.x1 + self.left_tail_offset * b.width
        yt_bot = sy + dc.v_overshoot

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
        draw_superellipse_loop(
            pen,
            sx,
            sy,
            b.x1,
            ymid - sy / 2,
            b.x2,
            b.y2,
            hx,
            hy * (1 - self.mid_height),
            cut="right",
        )
        draw_superellipse_loop(
            pen,
            sx,
            sy,
            b.x1,
            b.y1,
            b.x2,
            ymid + sy / 2,
            hx,
            hy * self.mid_height,
            cut="left",
        )
