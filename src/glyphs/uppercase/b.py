from glyph import Glyph
from shapes.superellipse_arch import draw_superellipse_arch
from shapes.rect import draw_rect


class UppercaseBGlyph(Glyph):
    name = "uppercase_b"
    unicode = "0x42"
    offset = 0
    loop_ratio = 0.6  # Horizontal split between left stem and loops
    upper_ratio = 0.9  # Upper loop width as a fraction of the lower loop width
    hx = 200  # Side curve radii (flatter than standard)
    hy = 140

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="ascent",
            overshoot_right=True,
        )
        arch_offset = 3 * dc.stroke / 4
        w = b.width / 2
        lower_x1 = b.x1 + (1 - self.loop_ratio) * w
        lower_x2 = b.x1 + (1 - self.loop_ratio * self.upper_ratio) * w
        upper_x2 = lower_x1 + (b.x2 - lower_x1) * self.upper_ratio
        cut_x = (lower_x1 + b.x2) / 2
        cut_x_up = (lower_x1 + upper_x2) / 2

        # Left stem
        draw_rect(pen, b.x1, 0, b.x1 + dc.stroke, dc.ascent)

        # Upper loop (narrower, displaced left)
        draw_superellipse_arch(
            pen,
            dc.stroke,
            lower_x1,
            b.ymid - dc.stroke / 2,
            upper_x2,
            b.y2,
            self.hx,
            self.hy,
            offset=arch_offset,
            side="bottom",
            cut="left",
        )
        # Lower loop (full width)
        draw_superellipse_arch(
            pen,
            dc.stroke,
            lower_x1,
            0,
            b.x2,
            b.ymid + dc.stroke / 2,
            self.hx,
            self.hy,
            offset=arch_offset,
            side="top",
            cut="left",
        )

        # Connecting bars
        draw_rect(pen, b.x1, b.y2 - dc.stroke, cut_x_up, b.y2)
        draw_rect(pen, b.x1, b.ymid - dc.stroke / 2, cut_x, b.ymid + dc.stroke / 2)
        draw_rect(pen, b.x1, 0, cut_x, dc.stroke)
