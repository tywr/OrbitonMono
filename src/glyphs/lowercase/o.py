from glyphs import Glyph
from draw.superellipse_loop import draw_superellipse_loop


class LowercaseOGlyph(Glyph):
    name = "lowercase_o"
    unicode = "0x6F"
    offset = 0
    stroke_x_ratio = 1.04
    stroke_y_ratio = 0.96

    def draw(
        self,
        pen,
        dc,
    ):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_left=True,
            overshoot_right=True,
        )
        sx, sy = self.stroke_x_ratio * dc.stroke_x, self.stroke_y_ratio * dc.stroke_y
        draw_superellipse_loop(pen, sx, sy, b.x1, b.y1, b.x2, b.y2, b.hx, b.hy)
