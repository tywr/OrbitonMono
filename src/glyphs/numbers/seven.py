from glyphs.numbers import NumberGlyph
from draw.rect import draw_rect
from draw.parallelogramm import draw_parallelogramm


class SevenGlyph(NumberGlyph):
    name = "seven"
    unicode = "0x37"
    offset = 5
    offset_foot = 0.2

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="cap", width_ratio=self.width_ratio, number=True
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio
        ox = self.offset_foot * b.width

        # Top bar
        draw_rect(pen, b.x1, b.y2 - sy, b.x2, b.y2)

        # Diagonal stroke
        theta, delta = draw_parallelogramm(
            pen,
            sx,
            sy,
            b.x1 + ox,
            b.y1,
            b.x2,
            b.y2 - sy - dc.gap,
        )
        draw_rect(pen, b.x2 - delta, b.y2 - sy - dc.gap, b.x2, b.y2)
