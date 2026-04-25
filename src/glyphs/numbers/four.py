from glyphs.numbers import NumberGlyph
from draw.rect import draw_rect
from draw.parallelogramm import draw_parallelogramm


class FourGlyph(NumberGlyph):
    name = "four"
    unicode = "0x34"
    offset = 6
    horizontal_ratio = 0.65
    vertical_ratio = 0.3
    mid_bar_ratio = 0.5
    width_ratio = 1.16

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="cap", width_ratio=self.width_ratio
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio

        xmid = b.x1 + self.horizontal_ratio * b.width
        ymid = b.y1 + self.vertical_ratio * b.height
        ybar = b.y1 + self.mid_bar_ratio * b.height

        theta, delta = draw_parallelogramm(
            pen, sx, sy, b.x1, ymid, xmid, b.y2
        )

        # Horizontal line
        draw_rect(pen, b.x1, ymid - sy, b.x2, ymid)

        # Vertical line
        draw_rect(pen, xmid - sx / 2, b.y1, xmid + sx / 2, ybar)
