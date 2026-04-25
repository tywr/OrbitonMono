from glyphs import Glyph
from draw.arch import draw_arch
from draw.rect import draw_rect
from draw.corner import draw_corner
from utils.intersection import intersection_superellipses


class SharpSGlyph(Glyph):
    name = "sharp_s"
    unicode = "0xdf"
    offset = 12
    upper_ratio = 0.9  # Upper loop width as a fraction of the lower loop width
    mid_ratio = 0.52
    width_ratio = 1.06
    offset_lower_bar = 0.3
    reach_upper_bar = 0.9
    tail_reach = 0.15
    stroke_x_ratio = 1.00
    stroke_y_ratio = 1.00

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            uppercase=True,
            width_ratio=self.width_ratio,
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio
        hx, hy = b.hx, b.hy
        ymid = b.y1 + self.mid_ratio * b.height
        xu = b.x1 + self.reach_upper_bar * b.width
        o = self.offset_lower_bar * b.width
        yt = -self.tail_reach * b.height

        lower_x1 = b.x1
        lower_x2 = b.x2
        lower_width = lower_x2 - lower_x1
        upper_width = self.upper_ratio * lower_width
        delta = lower_width - upper_width
        upper_x1 = lower_x1 + delta / 2
        upper_x2 = lower_x2 - delta / 2

        # Left stem
        draw_rect(pen, b.x1, yt, b.x1 + sx, (ymid - sy / 2 + b.y2) / 2)

        draw_corner(
            pen,
            sx,
            sy,
            b.x1,
            (ymid - sy / 2 + b.y2) / 2,
            (upper_x1 + upper_x2) / 2,
            b.y2,
            hx * (upper_x2 - upper_x1) / b.width,
            hy * (1 - self.mid_ratio),
            orientation="top-right",
        )
        arch1 = draw_arch(
            pen,
            sx,
            sy,
            upper_x1,
            ymid - sy / 2,
            upper_x2,
            b.y2,
            hx * (upper_x2 - upper_x1) / b.width,
            hy * (1 - self.mid_ratio),
            taper=0.75,
            side="bottom",
            cut="left",
        )

        # Lower loop (full width)
        arch2 = draw_arch(
            pen,
            sx,
            sy,
            lower_x1,
            0,
            lower_x2,
            ymid + sy / 2,
            hx,
            hy * self.mid_ratio,
            taper=0.75,
            cut="left",
            side="top",
        )

        # Compute the intersection of the two outer superellipses
        # where there would be a dc.gap sized gap
        intersection_x = max(
            intersection_superellipses(
                arch1["outer"], arch2["outer"].translate(dy=dc.gap)
            ),
            key=lambda x: x[0],
        )[0]

        draw_rect(
            pen,
            b.x1 + o,
            ymid - sy / 2,
            intersection_x,
            ymid + sy / 2,
        )
        draw_rect(
            pen,
            b.x1 + o,
            b.y1,
            (lower_x1 + lower_x2) / 2,
            b.y1 + sy,
        )
