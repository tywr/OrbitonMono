from glyphs import Glyph
from draw.superellipse_arch import draw_superellipse_arch
from draw.rect import draw_rect
from draw.polygon import draw_polygon


class LowercaseHGlyph(Glyph):
    name = "lowercase_h"
    unicode = "0x68"
    offset = 0
    width_ratio = 1.00
    top_stroke_y = 0.96
    hx_ratio = 1.25
    taper = 0.4

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_top=True,
            width_ratio=self.width_ratio,
        )

        # Top arch, cut at the bottom (only upper half drawn)
        arch_params = draw_superellipse_arch(
            pen,
            dc.stroke_x,
            self.top_stroke_y * dc.stroke_y,
            b.x1,
            b.y2 - b.height,
            b.x2,
            b.y2,
            1.1 * b.hx,
            b.hy,
            taper=self.taper,
            side="left",
            cut="bottom",
        )
        # Left stem — full ascent height with gap at the top
        draw_rect(pen, b.x1, 0, b.x1 + dc.stroke_x, dc.ascent)

        # Compute the intersection and fill the gap
        (_, y1), (_, y2) = arch_params["outer"].intersection_x(
            x=b.x1 + dc.stroke_x + dc.gap
        )
        _, y2 = min(y1, y2), max(y1, y2)

        # Fill the gap
        draw_polygon(
            pen,
            points=[
                (b.x1 + dc.stroke_x + dc.gap, y2),
                (b.x1 + dc.stroke_x, y2),
                (b.x1 + dc.stroke_x - dc.stroke_x * dc.taper / 2, b.ymid),
            ],
        )

        # Right stem — reaches up to the arch midpoint
        draw_rect(pen, b.x2 - dc.stroke_x, 0, b.x2, b.y1 + b.height / 2)
