from glyphs.uppercase import UppercaseGlyph
from draw.superellipse_arch import draw_superellipse_arch
from draw.rect import draw_rect
from utils.intersection import intersection_superellipses


class UppercaseBGlyph(UppercaseGlyph):
    name = "uppercase_b"
    unicode = "0x42"
    offset = 10
    upper_ratio = 0.9  # Upper loop width as a fraction of the lower loop width

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_right=True,
            uppercase=True,
            width_ratio=self.width_ratio,
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio
        hx, hy = dc.hx, dc.hy * 0.5 * dc.cap / dc.x_height

        lower_x1 = b.x1
        lower_x2 = b.x2
        lower_width = lower_x2 - lower_x1
        upper_width = self.upper_ratio * lower_width
        delta = lower_width - upper_width
        upper_x1 = lower_x1 + delta / 2
        upper_x2 = lower_x2 - delta / 2

        # Left stem
        draw_rect(pen, b.x1, 0, b.x1 + sx, dc.cap)

        # Upper loop (narrower, displaced left)
        arch1 = draw_superellipse_arch(
            pen,
            sx,
            sy,
            upper_x1,
            b.ymid - sy / 2,
            upper_x2,
            b.y2,
            hx,
            hy,
            taper=0.75,
            side="bottom",
            cut="left",
        )
        # Lower loop (full width)
        arch2 = draw_superellipse_arch(
            pen,
            sx,
            sy,
            lower_x1,
            0,
            lower_x2,
            b.ymid + sy / 2,
            hx,
            hy,
            taper=0.75,
            side="top",
            cut="left",
        )

        # Compute the intersection of the two outer superellipses
        # where there would be a dc.gap sized gap
        intersection_x = max(
            intersection_superellipses(
                arch1["outer"], arch2["outer"].translate(dy=dc.gap)
            ),
            key=lambda x: x[0],
        )[0]

        # Connecting bars
        draw_rect(pen, b.x1, b.y2 - sy, upper_x2 - upper_width / 2, b.y2)
        draw_rect(pen, b.x1, 0, b.x2 - lower_width / 2, sy)
        draw_rect(
            pen,
            b.x1,
            b.ymid - sy / 2,
            intersection_x,
            b.ymid + sy / 2,
        )
