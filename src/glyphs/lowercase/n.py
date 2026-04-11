from glyphs import Glyph
from draw.superellipse_arch import draw_superellipse_arch
from draw.rect import draw_rect


class LowercaseNGlyph(Glyph):
    name = "lowercase_n"
    unicode = "0x6E"
    offset = 0
    width_ratio = 1.00

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_top=True,
            overshoot_bottom=True,
            width_ratio=self.width_ratio,
        )

        # Top arch, cut at the bottom (only upper half drawn)
        arch_params = draw_superellipse_arch(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y2 - b.height,
            b.x2,
            b.y2,
            b.hx,
            b.hy,
            taper=dc.taper,
            side="left",
            cut="bottom",
        )
        # Left step
        draw_rect(pen, b.x1, 0, b.x1 + dc.stroke_x - dc.gap, dc.x_height)

        # Compute the intersection and fill the gap
        (_, y1), (_, y2) = arch_params["outer"].intersection_x(x=b.x1 + dc.stroke_x)
        y1, y2 = min(y1, y2), max(y1, y2)
        draw_rect(pen, b.x1, 0, b.x1 + dc.stroke_x, y2)

        # Right stem — reaches up to the arch midpoint
        draw_rect(pen, b.x2 - dc.stroke_x, 0, b.x2, b.y2 - b.height / 2)
