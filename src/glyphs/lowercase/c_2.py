from glyphs import Glyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.parallelogramm import draw_parallelogramm_vertical


class LowercaseC2Glyph(Glyph):
    name = "lowercase_c_2"
    font_feature = {"ss08": 1}
    unicode = "0x63"
    offset = 24
    stroke_x_ratio = 1.1
    stroke_y_ratio = 1.01
    hy_ratio = 1
    hx_ratio = 1
    width_ratio = 1
    len_tails = 0.35

    def draw(self, pen, dc):

        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_left=True,
            overshoot_right=True,
            width_ratio=self.width_ratio,
        )
        sx, sy = self.stroke_x_ratio * dc.stroke_x, self.stroke_y_ratio * dc.stroke_y
        hx, hy = self.hx_ratio * b.hx, self.hy_ratio * b.hy
        xt = b.xmid + self.len_tails * b.width
        yt_top = dc.x_height - sy - dc.v_overshoot
        yt_bot = sy + dc.v_overshoot

        draw_superellipse_loop(pen, sx, sy, b.x1, b.y1, b.x2, b.y2, hx, hy, cut="right")
        draw_parallelogramm_vertical(
            pen, sx, sy, b.xmid, b.y2, xt, yt_top, delta=sy, direction="bottom-right"
        )
        draw_parallelogramm_vertical(
            pen, sx, sy, b.xmid, b.y1, xt, yt_bot, delta=sy, direction="top-right"
        )
