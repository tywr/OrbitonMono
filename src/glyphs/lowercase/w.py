from math import atan, cos, sin
from glyph import Glyph
from shapes.polygon import draw_polygon
from shapes.parallelogramm import draw_parallelogramm


class LowercaseWGlyph(Glyph):
    name = "lowercase_w"
    unicode = "0x77"
    offset = 0
    overlap = 0.06
    width_ratio = 1.4
    inner_stroke_ratio = 0.9
    inner_height_ratio = 0.7
    inner_angle_ratio = 0.25

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, width_ratio=self.width_ratio)

        ov = self.overlap * b.width
        inner_height = self.inner_height_ratio * b.height
        theta, delta = draw_parallelogramm(
            pen,
            dc.stroke,
            b.xmid + self.inner_angle_ratio * b.width,
            0,
            b.x2,
            b.y2,
        )
        draw_parallelogramm(
            pen,
            dc.stroke,
            b.xmid - self.inner_angle_ratio * b.width,
            0,
            b.x1,
            b.y2,
            direction="top-left",
        )
        draw_parallelogramm(
            pen,
            dc.stroke * self.inner_stroke_ratio,
            b.xmid + self.inner_angle_ratio * b.width - ov + delta,
            0,
            b.xmid - ov,
            inner_height,
            direction="top-left",
        )
        draw_parallelogramm(
            pen,
            dc.stroke * self.inner_stroke_ratio,
            b.xmid - self.inner_angle_ratio * b.width + ov - delta,
            0,
            b.xmid + ov,
            inner_height,
        )
