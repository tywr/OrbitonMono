from glyphs import Glyph
from draw.superellipse_arch import draw_superellipse_arch
from draw.rect import draw_rect


class LowercaseUGlyph(Glyph):
    name = "lowercase_u"
    unicode = "0x75"
    offset = 0
    width_ratio = 1.00

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            width_ratio=self.width_ratio,
        )
        arch_top = b.y2

        # Bottom arch, cut at top (only lower half drawn)
        arch_params = draw_superellipse_arch(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1,
            b.x2,
            arch_top,
            b.hx,
            b.hy,
            taper=dc.taper,
            side="right",
            cut="top",
        )

        # Compute the intersection of the outer bowl with the stem
        (_, y1), (_, y2) = arch_params["outer"].intersection_x(x=b.x2 - dc.stroke_x)
        y1, y2 = min(y1, y2), max(y1, y2)

        # Right stem — full x_height with gap at baseline
        draw_rect(pen, b.x2 - dc.stroke_x, y1, b.x2, dc.x_height)
        draw_rect(pen, b.x2 - dc.stroke_x + dc.gap, 0, b.x2, dc.x_height)

        # Left stem — starts from arch midpoint
        draw_rect(pen, b.x1, (arch_top + b.y1) / 2, b.x1 + dc.stroke_x, dc.x_height)
