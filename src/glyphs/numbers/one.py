from glyphs.numbers import NumberGlyph
from draw.rect import draw_rect
from draw.parallelogramm import draw_parallelogramm_vertical


class OneGlyph(NumberGlyph):
    name = "one"
    unicode = "0x31"
    offset = -45
    branch_height = 0.32
    width_ratio = 0.65

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="cap", width_ratio=self.width_ratio, number=True
        )

        # Vertical stem (centered)
        draw_rect(pen, b.x2 - dc.stroke_x, b.y1, b.x2, b.y2)

        draw_parallelogramm_vertical(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1 + b.height * (1 - self.branch_height),
            b.x2 - dc.stroke_x,
            b.y2,
        )
