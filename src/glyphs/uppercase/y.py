from math import cos, sin, tan, pi

from glyphs.uppercase import UppercaseGlyph
from draw.parallelogramm import draw_parallelogramm
from draw.rect import draw_rect
from draw.polygon import draw_polygon


class UppercaseYGlyph(UppercaseGlyph):
    name = "uppercase_y"
    unicode = "0x59"
    offset = 0
    width_ratio = 1.3
    junction_ratio = 0.4
    overlap = 0.35

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, width_ratio=self.width_ratio, height="cap"
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio

        ov = self.overlap * sx
        yj = b.x1 + self.junction_ratio * b.height

        theta, delta = draw_parallelogramm(
            pen, sx, sy, b.xmid - ov, yj, b.x2, b.y2
        )
        draw_parallelogramm(
            pen,
            sx,
            sy,
            b.xmid + ov,
            yj,
            b.x1,
            b.y2,
            direction="top-left",
        )

        # Draw main step
        h = dc.gap / (2 * tan(0.5 * pi - theta))
        p = ov * tan(theta)
        draw_rect(pen, b.xmid - sx / 2, b.y1, b.xmid + sx / 2, yj + p + h)

        # Draw junction to fill the gaps
        draw_polygon(
            pen,
            points=[
                (b.xmid + ov - delta, yj),
                (b.xmid + ov - delta + (delta - ov) * cos(theta), yj - (delta - ov) * sin(theta)),
                (b.xmid, yj),
            ],
        )
        draw_polygon(
            pen,
            points=[
                (b.xmid, yj),
                (b.xmid - ov + delta - (delta - ov) * cos(theta), yj - (delta - ov) * sin(theta)),
                (b.xmid - ov + delta, yj),
            ],
        )
