from glyphs.uppercase import UppercaseGlyph
from draw.loop import draw_loop
from draw.square_corner import draw_square_corner


class UppercaseQGlyph(UppercaseGlyph):
    name = "uppercase_q"
    unicode = "0x51"
    offset = 0
    tail_width = 0.45
    tail_height = 0.2
    width_ratio = 1.08

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_bottom=True,
            overshoot_top=True,
            width_ratio=self.width_ratio,
            uppercase=True,
        )

        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio
        xe = b.xmid + self.tail_width * b.width
        ye = - self.tail_height * b.height

        draw_loop(
            pen,
            sx,
            sy,
            b.x1,
            b.y1,
            b.x2,
            b.y2,
            b.hx,
            b.hy,
        )

        draw_square_corner(
            pen,
            sx,
            sy,
            b.xmid - sx / 2,
            b.y1 + sy / 2,
            xe,
            ye,
        )
