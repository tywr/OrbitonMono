from math import cos, sin
from glyphs.numbers import NumberGlyph
from draw.rect import draw_rect
from draw.parallelogramm import draw_parallelogramm
from draw.cross_curve import draw_cross_curve_2
from draw.superellipse_loop import draw_superellipse_loop


class TwoGlyph(NumberGlyph):
    name = "two"
    unicode = "0x32"
    offset = 0
    hx_ratio = 0.78
    xj_ratio = 0.68
    yj_ratio = 0.45
    internal_radius = 0.2
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
        eh, ih = self.external_radius * b.height, self.internal_radius * b.height

        # Top arch
        params = draw_superellipse_loop(
            pen,
            sx,
            sx,
            b.x1,
            b.ymid,
            b.x2,
            b.y2,
            b.hx * self.hx_ratio,
            b.hy / 2,
            cut="bottom",
        )
        ishy = params["inner"].hy
        oshy = params["outer"].hy

        theta, delta = draw_parallelogramm(
            pen,
            sy,
            sy,
            b.x1,
            b.y1 + sy + dc.gap,
            xj,
            yj,
        )

        ehx, ehy = eh * cos(theta), eh * sin(theta)
        ihx, ihy = ih * cos(theta), ih * sin(theta)

        pen.moveTo((xj, yj))
        pen.curveTo((xj + ehx, yj + ehy), (b.x2, yt - oshy), (b.x2, yt))
        pen.lineTo((b.x2 - sx, yt))
        pen.curveTo(
            (b.x2 - sx, yt - ishy),
            (xj - delta + ihx, yj + ihy),
            (xj - delta, yj),
        )
        pen.closePath()

        # Bottom bar
        draw_rect(pen, b.x1, 0, b.x2, sy)
        draw_rect(pen, b.x1, b.y1 + sy, b.x1 + delta, b.y1 + sy + dc.gap)
