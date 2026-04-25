from glyphs import Glyph
from draw.arch import draw_arch
from draw.rect import draw_rect
from draw.polygon import draw_polygon


class LowercaseM2Glyph(Glyph):
    name = "lowercase_m_2"
    font_feature = {"cv01": 1}
    unicode = "0x6D"
    offset = 0
    width_ratio = 1.18
    top_stroke_y = 0.96
    hx_ratio = 0.82
    taper = 0.52
    ending_thickness = 0.75

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_top=True,
            width_ratio=self.width_ratio,
            min_margin=dc.min_margin,
        )
        mid_offset = ((1 + self.taper * dc.taper) * dc.stroke_x - dc.gap) / 2
        hx, hy = b.hx * self.hx_ratio, b.hy

        # Left arch (x1 to xmid) and store offset_x

        arch_params = draw_arch(
            pen,
            dc.stroke_x,
            self.top_stroke_y * dc.stroke_y,
            b.x1,
            b.y1,
            b.xmid + mid_offset,
            b.y2,
            hx,
            hy,
            taper=self.taper * dc.taper,
            side="left",
            cut="m_junction",
        )

        # Right arch (xmid to x2)
        draw_arch(
            pen,
            dc.stroke_x,
            self.top_stroke_y * dc.stroke_y,
            b.xmid - mid_offset,
            b.y1,
            b.x2,
            b.y2,
            hx,
            hy,
            taper=self.taper * dc.taper,
            side="left",
            cut="bottom",
        )

        # Compute the intersection and fill the gap
        (_, y1), (_, y2) = arch_params["outer"].intersection_x(x=b.x1 + dc.stroke_x)
        y1, y2 = min(y1, y2), max(y1, y2)

        # Left stem
        draw_rect(pen, b.x1, 0, b.x1 + dc.stroke_x, y2)
        draw_polygon(
            pen,
            points=[
                (b.x1 + self.ending_thickness * dc.stroke_x, dc.x_height),
                (b.x1, dc.x_height),
                (b.x1, y2),
                (b.x1 + dc.stroke_x - dc.gap, y2),
            ],
        )

        # Right foot — reaches up to the arch midpoint
        draw_rect(pen, b.x2 - dc.stroke_x, 0, b.x2, b.ymid)

        # Middle stem extension
        draw_rect(
            pen,
            b.xmid - (1 - self.taper * dc.taper) * dc.stroke_x / 2 - dc.gap / 2,
            0,
            b.xmid + (1 - self.taper * dc.taper) * dc.stroke_x / 2 + dc.gap / 2,
            y2,
        )
