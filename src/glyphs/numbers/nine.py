from glyphs.numbers import NumberGlyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.superellipse_arch import draw_superellipse_arch
from draw.rect import draw_rect
from draw.smooth_corner import draw_smooth_corner
from draw.polygon import draw_polygon


class NineGlyph(NumberGlyph):
    name = "nine"
    unicode = "0x39"
    offset = 0
    vertical_ratio = 0.6
    bottom_cut = 0.2
    taper = 0.3
    hx_ratio = 0.78

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

        # Upper loop
        params = draw_superellipse_arch(
            pen,
            sx,
            sy,
            b.x1,
            ymid,
            b.x2,
            b.y2,
            b.hx * self.hx_ratio,
            b.hy * self.vertical_ratio,
            taper=self.taper,
            side="right",
            cut="top",
        )

        # Compute the intersection and fill the gap
        (_, y1), (_, y2) = params["outer"].intersection_x(x=b.x2 - sx - dc.gap)
        yj = min(y1, y2)

        draw_polygon(
            pen,
            points=[
                (b.x2 - sx - dc.gap, yj),
                (b.x2 - sx, yj),
                (b.x2 - sx / 2, (b.y2 + ymid) / 2),
            ],
        )

        draw_superellipse_loop(
            pen,
            sx,
            sy,
            b.x1,
            ymid,
            b.x2,
            b.y2,
            b.hx * self.hx_ratio,
            b.hy * self.vertical_ratio,
            cut="bottom",
        )
        draw_rect(pen, b.x2 - sx, b.ymid, b.x2, b.y2 - (b.y2 - ymid) / 2)

        draw_smooth_corner(
            pen,
            sx,
            sy,
            b.x2,
            b.ymid,
            b.xmid,
            b.y1,
            b.hx * self.hx_ratio,
            b.hy,
            orientation="bottom-left",
        )
        draw_rect(
            pen,
            b.x1 + 0.6 * sx,
            b.y1,
            b.xmid,
            b.y1 + sy,
        )
