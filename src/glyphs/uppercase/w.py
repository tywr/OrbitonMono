from math import tan, pi
from glyphs import Glyph
from draw.parallelogramm import draw_parallelogramm
from draw.rect import draw_rect


class UppercaseWGlyph(Glyph):
    name = "uppercase_w"
    unicode = "0x57"
    offset = 0
    outer_overlap = 0.142
    inner_overlap = 0.15
    width_ratio = 1.25
    inner_stroke_ratio = 0.85
    inner_height_ratio = 0.55
    inner_angle_ratio = 0.26

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, width_ratio=self.width_ratio, height="cap"
        )
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

        # Fill the outer gaps
        x = 1 / (1 + tan(theta) / tan(theta2))
        p = x * (ov * tan(theta))
        h = dc.gap * p / ov
        draw_rect(
            pen,
            b.xmid + self.inner_angle_ratio * b.width - delta2 / 2,
            b.y1,
            b.xmid + self.inner_angle_ratio * b.width + delta2 / 2,
            b.y1 + p + h,
        )
        draw_rect(
            pen,
            b.xmid - self.inner_angle_ratio * b.width - delta2 / 2,
            b.y1,
            b.xmid - self.inner_angle_ratio * b.width + delta2 / 2,
            b.y1 + p + h,
        )

        # Fill the inside gap
        h = dc.gap / (2 * tan(0.5 * pi - theta2))
        p = ovi * tan(theta2)
        draw_rect(
            pen,
            b.xmid - ovi,
            inner_height - p - h,
            b.xmid + ovi,
            inner_height,
        )
