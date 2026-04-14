from glyphs import Glyph
from draw.superellipse_arch import draw_superellipse_arch
from draw.rect import draw_rect
from draw.polygon import draw_polygon


class LowercaseRGlyph(Glyph):
    name = "lowercase_r"
    unicode = "0x72"
    offset = 20
    loop_ratio = 0.8
    width_ratio = 1.02
    top_stroke_y = 0.96

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, overshoot_top=True, overshoot_right=True, width_ratio=self.width_ratio)
        hx, hy = dc.hx, dc.hy * self.loop_ratio

        # Top arch, cut at the bottom (only upper half drawn)
        arch_params = draw_superellipse_arch(
            pen,
            dc.stroke_x,
            self.top_stroke_y * dc.stroke_y,
            b.x1,
            b.y2 - b.height * self.loop_ratio,
            b.x2,
            b.y2,
            hx,
            hy,
            taper=dc.taper_r,
            side="left",
            cut="bottom",
        )

        # Compute the intersection of the outer bowl with the stem
        (_, y1), (_, y2) = arch_params["outer"].intersection_x(x=b.x1 + dc.stroke_x + dc.gap)
        y1, y2 = min(y1, y2), max(y1, y2)

        # Fill the gap
        draw_polygon(
            pen,
            points=[
                (b.x1 + dc.stroke_x + dc.gap, y2),
                (b.x1 + dc.stroke_x, y2),
                (b.x1 + dc.stroke_x - dc.stroke_x * dc.taper / 2, b.ymid),
            ],
        )

        # Left stem
        draw_rect(pen, b.x1, 0, b.x1 + dc.stroke_x, dc.x_height)
