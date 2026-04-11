from glyphs.uppercase import UppercaseGlyph
from draw.rect import draw_rect
from draw.parallelogramm import draw_parallelogramm


class UppercaseZGlyph(UppercaseGlyph):
    name = "uppercase_z"
    unicode = "0x5A"
    offset = 0
    wdith_ratio = 1.08

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, height="cap", width_ratio=self.width_ratio)

        # Top and bottom bars
        draw_rect(pen, b.x1, b.y2 - dc.stroke_y, b.x2, b.y2)
        draw_rect(pen, b.x1, 0, b.x2, dc.stroke_y)

        # Diagonal stroke
        draw_parallelogramm(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1 + dc.stroke_y,
            b.x2,
            b.y2 - dc.stroke_y,
        )
