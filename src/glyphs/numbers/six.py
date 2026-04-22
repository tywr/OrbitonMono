from math import cos, sin
from glyphs.numbers import NumberGlyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.superellipse_arch import draw_superellipse_arch
from draw.polygon import draw_polygon
from draw.parallelogramm import draw_parallelogramm
from utils.pens import NullPen


class SixGlyph(NumberGlyph):
    name = "six"
    unicode = "0x36"
    offset = 0
    loop_ratio = 0.6
    top_ratio = 0.4
    taper = 0.4
    cap_x = 0.9
    joint_x = 1.4

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_bottom=True,
            overshoot_left=True,
            overshoot_right=True,
            width_ratio=self.width_ratio,
            number=True,
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio

        ymid = b.y1 + self.loop_ratio * b.height
        xc = b.x1 + self.cap_x * b.width
        xj = b.x1 + self.joint_x * sx + dc.gap

        # Bottom loop
        params = draw_superellipse_arch(
            pen,
            sx,
            sy,
            b.x1,
            b.y1,
            b.x2,
            ymid,
            b.hx,
            b.hy * self.loop_ratio,
            taper=self.taper,
            side="left",
            cut="bottom",
        )

        # Compute the intersection and fill the gap
        (_, y1), (_, y2) = params["outer"].intersection_x(x=xj)
        yj = max(y1, y2)

        theta, delta = draw_parallelogramm(
            NullPen(),
            sx,
            sy,
            xj,
            yj,
            xc,
            b.y2,
        )

        draw_polygon(
            pen,
            points=[
                (xj, yj),
                (xj - dc.gap - delta / 2, yj),
                (b.x1, (b.y1 + ymid) / 2),
                (b.x1 + sx, (b.y1 + ymid) / 2),
                (b.x1 + sx, (b.y1 + ymid) / 2 + sy / 2),
            ],
        )

        lp = ((b.y2 - yj) ** 2 + (xj - xc) ** 2) ** 0.5
        dx = lp * cos(theta)
        dy = lp * sin(theta)
        xcm, ycm = xj - dc.gap - delta + 0.66 * dx, yj + 0.66 * dy
        xcp, ycp = xj - dc.gap - delta + 0.33 * dx, yj + 0.33 * dy

        pen.moveTo((xj - dc.gap, yj))
        pen.lineTo((xc - delta - dc.gap, b.y2))
        pen.lineTo((xc - 2 * delta - dc.gap, b.y2))
        pen.lineTo((xcm, ycm))
        pen.curveTo(
            (xcp, ycp),
            (b.x1, (b.y1 + ymid) / 2 + b.hx),
            (b.x1, (b.y1 + ymid) / 2),
        )
        pen.lineTo((b.x1 + sx / 2, (b.y1 + ymid) / 2))
        pen.closePath()

        draw_superellipse_loop(
            pen,
            sx,
            sy,
            b.x1,
            b.y1,
            b.x2,
            ymid,
            b.hx,
            b.hy * self.loop_ratio,
            cut="top",
        )
