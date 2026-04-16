from glyphs.numbers import NumberGlyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.superellipse_arch import draw_superellipse_arch
from draw.rect import draw_rect
from draw.smooth_corner import draw_smooth_corner
from draw.polygon import draw_polygon


class SixGlyph(NumberGlyph):
    name = "six"
    unicode = "0x36"
    offset = 0
    loop_ratio = 0.6
    top_ratio = 0.4
    top_cut = 0.8
    taper = 0.2
    hx_ratio = 0.78

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
        ytop = b.y1 + self.top_ratio * b.height
        ycut = b.y1 + self.top_cut * b.height

        # Bottom loop
        params = draw_superellipse_arch(
            pen,
            sx,
            sy,
            b.x1,
            b.y1,
            b.x2,
            ymid,
            b.hx * self.hx_ratio,
            b.hy * self.loop_ratio,
            taper=self.taper,
            side="left",
            cut="bottom",
        )

        # Compute the intersection and fill the gap
        (_, y1), (_, y2) = params["outer"].intersection_x(x=b.x1 + sx + dc.gap)
        yj = max(y1, y2)

        draw_polygon(
            pen,
            points=[
                (b.x1 + sx + dc.gap, yj),
                (b.x1 + sx, yj),
                (b.x1 + sx / 2, (b.y1 + ymid) / 2),
            ],
        )

        draw_superellipse_loop(
            pen,
            sx,
            sy,
            b.x1,
            b.y1,
            b.x2,
            ymid,
            b.hx * self.hx_ratio,
            b.hy * self.loop_ratio,
            cut="top",
        )
        draw_rect(
            pen,
            b.x1,
            b.y1 + (ymid - b.y1) / 2,
            b.x1 + sx,
            b.ymid,
        )
        draw_smooth_corner(
            pen,
            sx,
            sy,
            b.x1,
            b.ymid,
            b.xmid,
            b.y2,
            b.hx * self.hx_ratio,
            b.hy,
            orientation="top-right",
        )
        draw_rect(
            pen,
            b.xmid,
            b.y2 - sy,
            b.x2 - 0.6 * sx,
            b.y2,
        )
