from math import sin, cos, pi
from glyphs.numbers import NumberGlyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.arch import draw_arch
from draw.polygon import draw_polygon
from draw.parallelogramm import draw_parallelogramm
from utils.pens import NullPen


class NineGlyph(NumberGlyph):
    name = "nine"
    unicode = "0x39"
    offset = 0
    vertical_ratio = 0.6
    bottom_cut = 0.2
    taper = 0.8
    foot_x = 0.05
    joint_x = 1.4

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_top=True,
            overshoot_left=True,
            overshoot_right=True,
            width_ratio=self.width_ratio,
            number=True,
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio
        ymid = b.y2 - self.vertical_ratio * b.height

        xf = b.x1 + self.foot_x * b.width
        xj = b.x2 - self.joint_x * sx - dc.gap

        # Upper loop
        params = draw_arch(
            pen,
            sx,
            sy,
            b.x1,
            ymid,
            b.x2,
            b.y2,
            b.hx,
            b.hy * self.vertical_ratio,
            taper=self.taper * dc.taper,
            side="right",
            cut="top",
        )

        # Compute the intersection and fill the gap
        (_, y1), (_, y2) = params["outer"].intersection_x(x=xj)
        yj = min(y1, y2)

        # Draw dummy parallelogramm to get the angle
        theta, delta = draw_parallelogramm(
            NullPen(), sx, sy, xj, yj, xf, b.y1, direction="bottom-left"
        )

        draw_polygon(
            pen,
            points=[
                (xj, yj),
                (xj + dc.gap, yj),
                (b.x2, (b.y2 + ymid) / 2),
                (b.x2 - sx, (b.y2 + ymid) / 2),
                (b.x2 - sx, (b.y2 + ymid) / 2 - sy / 2),
            ],
        )

        lp = ((b.y1 - yj) ** 2 + (xj - xf) ** 2) ** 0.5
        dx = lp * cos(theta)
        dy = lp * sin(theta)
        xcm, ycm = xj + dc.gap + delta - 0.66 * dx, yj - 0.66 * dy
        xcp, ycp = xj + dc.gap + delta - 0.33 * dx, yj - 0.33 * dy

        pen.moveTo((xj + dc.gap, yj))
        pen.lineTo((xf + delta + dc.gap, b.y1))
        pen.lineTo((xf + 2 * delta + dc.gap, b.y1))
        pen.lineTo((xcm, ycm))
        pen.curveTo(
            (xcp, ycp),
            (b.x2, (b.y2 + ymid) / 2 - b.hx),
            (b.x2, (b.y2 + ymid) / 2),
        )

        draw_superellipse_loop(
            pen,
            sx,
            sy,
            b.x1,
            ymid,
            b.x2,
            b.y2,
            b.hx,
            b.hy * self.vertical_ratio,
            cut="bottom",
        )
