from glyphs.numbers import NumberGlyph
from draw.rect import draw_rect
from draw.parallelogramm import draw_parallelogramm


class FourGlyph(NumberGlyph):
    name = "four"
    unicode = "0x34"
    offset = -5
    horizontal_ratio = 0.65
    vertical_ratio = 0.3
    mid_bar_ratio = 0.5
    width_ratio = 1.16

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="cap", width_ratio=self.width_ratio
        )

        xmid = b.x1 + self.horizontal_ratio * b.width
        ymid = b.y1 + self.vertical_ratio * b.height
        ybar = b.y1 + self.mid_bar_ratio * b.height

        theta, delta = draw_parallelogramm(
            pen, dc.stroke_x, dc.stroke_y, b.x1, ymid, xmid, b.y2
        )

        # Horizontal line
        draw_rect(pen, b.x1, ymid - dc.stroke_y, b.x2, ymid)

        # Vertical line
        draw_rect(pen, xmid - dc.stroke_x / 2, b.y1, xmid + dc.stroke_x / 2, ybar)
