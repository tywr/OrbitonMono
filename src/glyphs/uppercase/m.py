from math import tan, pi
from glyphs.uppercase import UppercaseGlyph
from draw.rect import draw_rect
from draw.parallelogramm import draw_parallelogramm


class UppercaseMGlyph(UppercaseGlyph):
    name = "uppercase_m"
    unicode = "0x4D"
    offset = 0
    width_ratio = 1.2
    overlap = 0.4
    overlap_middle = 0.5
    depth = 0.6
    stroke_thinning = 0.8

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="cap", width_ratio=self.width_ratio
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio
        st = self.stroke_thinning
        ov = self.overlap * dc.stroke_x
        ovm = self.overlap_middle * dc.stroke_x
        ymid = (1 - self.depth) * b.height

        # Vertical stems
        draw_rect(pen, b.x1, b.y1, b.x1 + sx, b.y2)
        draw_rect(pen, b.x2 - sx, b.y1, b.x2, b.y2)

        # Branches
        draw_parallelogramm(
            pen,
            st * sx,
            st * sy,
            b.xmid - ovm / 2,
            ymid,
            b.x2 - ov,
            b.y2,
        )
        theta, delta = draw_parallelogramm(
            pen,
            st * sx,
            st * sy,
            b.xmid + ovm / 2,
            ymid,
            b.x1 + ov,
            b.y2,
            direction="top-left",
        )

        # Fill the gap
        p = ovm * tan(theta) / 2
        h = p * dc.gap / ovm
        draw_rect(
            pen,
            b.xmid - ovm,
            ymid,
            b.xmid + ovm,
            ymid + p + h,
        )
