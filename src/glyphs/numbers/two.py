from math import cos, sin
from glyphs.numbers import NumberGlyph
from draw.rect import draw_rect
from draw.parallelogramm import draw_parallelogramm
from draw.superellipse_loop import draw_superellipse_loop
from utils.pens import NullPen


class TwoGlyph(NumberGlyph):
    name = "two"
    unicode = "0x32"
    offset = 0
    xj_ratio = 0.82
    yj_ratio = 0.55
    radius = 0.2
    internal_radius = 0.1
    external_radius = 0.1

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_top=True,
            width_ratio=self.width_ratio,
            number=True,
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio
        xj = b.x1 + self.xj_ratio * b.width + sx / 2
        yj = b.y1 + self.yj_ratio * b.height
        yt = (b.ymid + b.y2) / 2
        ih = self.internal_radius * b.height

        # Top arch
        params = draw_superellipse_loop(
            pen,
            sx,
            sx,
            b.x1,
            b.ymid,
            b.x2,
            b.y2,
            b.hx,
            b.hy / 2,
            cut="bottom",
        )
        ishy = params["inner"].hy
        oshy = params["outer"].hy

        theta, delta = draw_parallelogramm(
            NullPen(),
            sy,
            sy,
            b.x1,
            b.y1 + sy + dc.gap,
            xj,
            yj,
        )

        eps = theta
        px, py = delta * sin(eps) * cos(eps), delta * sin(eps) ** 2
        xl = xj - px
        yl = yj - py

        ihx, ihy = ih * cos(theta), ih * sin(theta)

        pen.moveTo((xl, yl))
        pen.curveTo((xl + ihx, yl + ihy), (b.x2, yt - oshy), (b.x2, yt))
        pen.lineTo((b.x2 - sx, yt))
        pen.curveTo(
            (b.x2 - sx, yt - ishy),
            (xj - delta + ihx, yj + ihy),
            (xj - delta, yj),
        )
        pen.lineTo((b.x1, b.y1 + sy + dc.gap))
        pen.lineTo((b.x1 + delta, b.y1 + sy + dc.gap))
        pen.closePath()

        # Bottom bar
        draw_rect(pen, b.x1, 0, b.x2, sy)
        draw_rect(pen, b.x1, b.y1 + sy, b.x1 + delta, b.y1 + sy + dc.gap)
