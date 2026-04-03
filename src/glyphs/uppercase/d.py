from glyph import Glyph
from shapes.corner import draw_corner
from shapes.rect import draw_rect


class UppercaseDGlyph(Glyph):
    name = "uppercase_d"
    unicode = "0x44"
    offset = 0
    width_ratio = 350 / 340
    loop_ratio = 0.6  # Horizontal split between left stem and curve
    hx = 200          # Side curve radii (flatter than standard)
    hy = 140

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="ascent",
            width_ratio=self.width_ratio,
            overshoot_right=True,
        )
        w = b.width / 2
        arch_x1 = b.x1 + (1 - self.loop_ratio) * w
        cut_x = (arch_x1 + b.x2) / 2

        # Left stem
        draw_rect(pen, b.x1, 0, b.x1 + dc.stroke, dc.ascent)
        # Right flat portion
        draw_rect(pen, b.x2 - dc.stroke, 0.25 * dc.ascent, b.x2, 0.75 * dc.ascent)
        # Connecting bars
        draw_rect(pen, b.x1, b.y2 - dc.stroke, cut_x, b.y2)
        draw_rect(pen, b.x1, 0, cut_x, dc.stroke)
        # Corner
        draw_corner(pen, dc.stroke, b.x2, 0.75 * dc.ascent, cut_x, b.y2, self.hx, self.hy, orientation="top-left")
