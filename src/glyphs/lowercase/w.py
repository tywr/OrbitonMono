from math import tan
from glyphs import Glyph
from draw.parallelogramm import draw_parallelogramm
from draw.rect import draw_rect


class LowercaseWGlyph(Glyph):
    name = "lowercase_w"
    unicode = "0x77"
    offset = 0
    outer_overlap = 0.155
    inner_overlap = 0.25
    width_ratio = 1.25
    inner_stroke_ratio = 0.75
    inner_height_ratio = 0.7
    inner_angle_ratio = 0.26

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, width_ratio=self.width_ratio)
        ov = self.outer_overlap * dc.stroke_x
        ovi = self.inner_overlap * dc.stroke_x

        inner_height = self.inner_height_ratio * b.height
        theta, delta = draw_parallelogramm(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.xmid + self.inner_angle_ratio * b.width,
            0,
            b.x2,
            b.y2,
        )
        draw_parallelogramm(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.xmid - self.inner_angle_ratio * b.width,
            0,
            b.x1,
            b.y2,
            direction="top-left",
        )
        theta2, delta2 = draw_parallelogramm(
            pen,
            self.inner_stroke_ratio * dc.stroke_x,
            self.inner_stroke_ratio * dc.stroke_y,
            b.xmid + self.inner_angle_ratio * b.width + ov,
            0,
            b.xmid - ovi,
            inner_height,
            direction="top-left",
        )
        draw_parallelogramm(
            pen,
            self.inner_stroke_ratio * dc.stroke_x,
            self.inner_stroke_ratio * dc.stroke_y,
            b.xmid - self.inner_angle_ratio * b.width - ov,
            0,
            b.xmid + ovi,
            inner_height,
        )

        # Fill the gaps
        x = 1 / (1 + tan(theta) / tan(theta2))
        p = x * (ov * tan(theta))
        h = dc.gap * p / ov
        print(b.y1 + p + h)
        draw_rect(
            pen,
            b.xmid + self.inner_angle_ratio * b.width - delta2 / 2,
            b.y1,
            b.xmid + self.inner_angle_ratio * b.width + ov,
            b.y1 + p + h,
        draw_rect(
            pen,
            b.xmid - self.inner_angle_ratio * b.width - ov,
            b.y1,
            b.xmid - self.inner_angle_ratio * b.width + delta2 / 2,
            b.y1 + p + h,
        )
        )
