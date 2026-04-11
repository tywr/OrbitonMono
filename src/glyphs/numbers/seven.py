from glyphs.numbers import NumberGlyph
from draw.rect import draw_rect
from draw.parallelogramm import draw_parallelogramm


class SevenGlyph(NumberGlyph):
    name = "seven"
    unicode = "0x37"
    offset = 5
    width_ratio = 1.1
    offset_foot = 0.2

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="cap", width_ratio=self.width_ratio
        )
        ox = self.offset_foot * b.width

        # Top bar
        draw_rect(pen, b.x1, b.y2 - dc.stroke_y, b.x2, b.y2)

        # Diagonal stroke
        draw_parallelogramm(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1 + ox,
            b.y1,
            b.x2,
            b.y2 - dc.stroke_y,
        )
