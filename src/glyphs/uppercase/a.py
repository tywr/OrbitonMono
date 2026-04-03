from math import atan, sin, cos
from glyph import Glyph
from shapes.polygon import draw_polygon


class UppercaseAGlyph(Glyph):
    name = "uppercase_a"
    unicode = "0x41"
    offset = 0
    width_ratio = 420 / 340
    bar_height = 320  # Absolute height of the crossbar

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, height="ascent", width_ratio=self.width_ratio)
        half_width = b.width / 2 - dc.stroke / 2

        branch_h = dc.ascent
        theta = atan(branch_h / half_width)
        x_delta = dc.stroke / sin(theta)

        # Right branch
        draw_polygon(
            pen,
            points=[
                (b.xmid + x_delta / 2, dc.ascent),
                (b.xmid + half_width + x_delta / 2, 0),
                (b.xmid + half_width - x_delta / 2, 0),
                (b.xmid - x_delta / 2, dc.ascent),
            ],
        )
        # Left branch
        draw_polygon(
            pen,
            points=[
                (b.xmid + x_delta / 2, dc.ascent),
                (b.xmid - half_width + x_delta / 2, 0),
                (b.xmid - half_width - x_delta / 2, 0),
                (b.xmid - x_delta / 2, dc.ascent),
            ],
        )
        # Crossbar
        draw_polygon(
            pen,
            points=[
                (b.xmid + half_width - self.bar_height * cos(theta), self.bar_height * sin(theta)),
                (b.xmid + half_width - (self.bar_height - dc.stroke) * cos(theta), (self.bar_height - dc.stroke) * sin(theta)),
                (b.xmid - half_width + (self.bar_height - dc.stroke) * cos(theta), (self.bar_height - dc.stroke) * sin(theta)),
                (b.xmid - half_width + self.bar_height * cos(theta), self.bar_height * sin(theta)),
            ],
        )
