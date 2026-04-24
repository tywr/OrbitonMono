from glyphs import Glyph
from draw.r_arch import draw_r_arch
from draw.superellipse_arch import draw_superellipse_arch
from draw.rect import draw_rect
from draw.polygon import draw_polygon
from draw.parallelogramm import draw_smooth_parallelogramm_vertical


class LowercaseRGlyph(Glyph):
    name = "lowercase_r"
    unicode = "0x72"
    offset = 10
    loop_ratio = 0.9
    hx_ratio = 1
    hy_ratio = 1
    taper = 0.4
    ending_thickness = 0.8
    width_ratio = 1

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_top=True,
            overshoot_right=True,
            width_ratio=self.width_ratio,
        )
        hx, hy = dc.hx * self.hx_ratio, dc.hy * self.hy_ratio
        ys = b.y2 - self.loop_ratio * b.height

        arch_params = draw_superellipse_arch(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            ys,
            b.x2,
            b.y2,
            hx,
            hy,
            taper=self.taper * dc.taper,
            side="left",
            cut="bottom",
        )

        # Compute the intersection of the outer bowl with the stem
        (_, y1), (_, y2) = arch_params["outer"].intersection_x(
            x=b.x1 + dc.stroke_x + dc.gap
        )
        y1, y2 = min(y1, y2), max(y1, y2)

        # Left stem
        draw_rect(pen, b.x1, 0, b.x1 + dc.stroke_x, y2)
        draw_polygon(
            pen,
            points=[
                (b.x1 + self.ending_thickness * dc.stroke_x, dc.x_height),
                (b.x1, dc.x_height),
                (b.x1, y2),
                (b.x1 + dc.stroke_x, y2),
            ],
        )

        # Fill the gap
        draw_polygon(
            pen,
            points=[
                (b.x1 + dc.stroke_x + dc.gap, y2),
                (b.x1 + dc.stroke_x, y2),
                (b.x1 + dc.stroke_x - dc.stroke_x * dc.taper * self.taper / 2, b.ymid),
            ],
        )

        # draw_smooth_parallelogramm_vertical(
        #     pen, dc.stroke_y, (b.x1 + xl) / 2, b.y2, b.x2, yt, direction="bottom-right"
        # )
