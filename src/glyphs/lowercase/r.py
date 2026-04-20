from glyphs import Glyph
from draw.r_arch import draw_r_arch
from draw.rect import draw_rect
from draw.polygon import draw_polygon
from draw.parallelogramm import draw_smooth_parallelogramm_vertical


class LowercaseRGlyph(Glyph):
    name = "lowercase_r"
    unicode = "0x72"
    offset = 14
    loop_ratio = 1.2
    width_ratio = 0.86
    top_stroke_y = 1
    hx_ratio = 1
    taper = 0.2
    ending_thickness = 0.8

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_top=True,
            overshoot_right=True,
            width_ratio=self.width_ratio,
        )
        hx, hy = dc.hx * self.hx_ratio, dc.hy * self.loop_ratio
        yt = dc.x_height - dc.stroke_y - dc.v_overshoot
        xl = self.loop_ratio * b.width + dc.stroke_x

        # Top arch, cut at the bottom (only upper half drawn)
        arch_params = draw_r_arch(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1,
            xl,
            b.y2,
            hx,
            hy,
            taper=self.taper,
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
                (b.x1 + dc.stroke_x - dc.stroke_x * dc.taper / 2, b.ymid),
            ],
        )

        draw_smooth_parallelogramm_vertical(
            pen, dc.stroke_y, (b.x1 + xl) / 2, b.y2, b.x2, yt, direction="bottom-right"
        )

        # Wing
        draw_rect(pen, b.x1, dc.x_height - dc.stroke_y, b.x1, dc.x_height)
