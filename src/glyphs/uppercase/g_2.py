from glyphs.uppercase import UppercaseGlyph
from draw.rect import draw_rect
from draw.superellipse_loop import draw_superellipse_loop
from draw.parallelogramm import draw_parallelogramm_vertical


class UppercaseG2Glyph(UppercaseGlyph):
    name = "uppercase_g_2"
    font_feature = {"ss08": 1}
    unicode = "0x47"
    offset = 2
    stroke_x_ratio = UppercaseGlyph.stroke_x_ratio * 1.01
    stroke_y_ratio = UppercaseGlyph.stroke_y_ratio * 1.1
    hy_ratio = 1
    hx_ratio = 1
    width_ratio = 1.06
    len_tails = 0.38
    mid_ratio = 0.5

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_left=True,
            overshoot_right=True,
            width_ratio=self.width_ratio,
            uppercase=True,
            height="cap",
        )
        sx, sy = self.stroke_x_ratio * dc.stroke_x, self.stroke_y_ratio * dc.stroke_y
        hx, hy = self.hx_ratio * b.hx, self.hy_ratio * b.hy
        xt = b.xmid + self.len_tails * b.width
        yt_top = dc.cap - sy - dc.v_overshoot
        ymid = b.y1 + self.mid_ratio * b.height

        draw_superellipse_loop(pen, sx, sy, b.x1, b.y1, b.x2, b.y2, hx, hy, cut="right")
        draw_superellipse_loop(pen, sx, sy, b.x1, b.y1, b.x2, b.y2, hx, hy, cut="top")
        draw_parallelogramm_vertical(
            pen, sx, sy, b.xmid, b.y2, xt, yt_top, delta=sy, direction="bottom-right"
        )

        draw_rect(
            pen,
            b.x2 - sx,
            b.ymid,
            b.x2,
            ymid,
        )
        draw_rect(
            pen,
            b.xmid,
            ymid,
            b.x2,
            ymid + sy / 2,
        )
        draw_rect(
            pen,
            b.xmid,
            ymid - sy / 2,
            b.x2 - sx / 2,
            ymid,
        )
