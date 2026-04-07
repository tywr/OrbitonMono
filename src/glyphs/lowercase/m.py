from glyphs import Glyph
from draw.superellipse_arch import draw_superellipse_arch
from draw.rect import draw_rect


class LowercaseMGlyph(Glyph):
    name = "lowercase_m"
    unicode = "0x6D"
    offset = 0
    width_ratio = 1.25
    mid_len = 0.6

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            width_ratio=self.width_ratio,
        )
        mid_y = b.y1 + (1 - self.mid_len) * b.height
        mid_offset = ((1 + dc.taper_m) * dc.stroke_x - dc.gap) / 2
        hx, hy = b.hx * (mid_offset + b.width / 2) / b.width, b.hy

        # Left arch (x1 to xmid) and store offset_x

        arch_params = draw_superellipse_arch(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1,
            b.xmid + mid_offset,
            b.y2,
            hx,
            hy,
            taper=dc.taper_m,
            side="left",
            cut="m_junction",
        )

        # Right arch (xmid to x2)
        draw_superellipse_arch(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.xmid - mid_offset,
            b.y1,
            b.x2,
            b.y2,
            hx,
            hy,
            taper=dc.taper_m,
            side="left",
            cut="bottom",
        )
        # Left foot
        draw_rect(pen, b.x1, 0, b.x1 + dc.stroke_x - dc.gap, dc.x_height)

        # Compute the intersection and fill the gap
        (_, y1), (_, y2) = arch_params["outer"].intersection_x(x=b.x1 + dc.stroke_x)
        y1, y2 = min(y1, y2), max(y1, y2)
        draw_rect(pen, b.x1, 0, b.x1 + dc.stroke_x, y2)

        # Right foot — reaches up to the arch midpoint
        draw_rect(pen, b.x2 - dc.stroke_x, 0, b.x2, b.ymid)

        # Middle stem extension
        draw_rect(
            pen,
            b.xmid - (1 - dc.taper_m) * dc.stroke_x / 2 - dc.gap / 2,
            mid_y,
            b.xmid + (1 - dc.taper_m) * dc.stroke_x / 2 + dc.gap / 2,
            y2,
        )
