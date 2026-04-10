from glyphs import Glyph
from draw.rect import draw_rect
from draw.superellipse_loop import draw_superellipse_loop


class LeftParenthesisGlyph(Glyph):
    name = "left_parenthesis"
    unicode = "0x28"
    offset = 0
    width_ratio = 0.4

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="x_height", width_ratio=self.width_ratio
        )
        ymid = dc.parenthesis
        draw_superellipse_loop(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            ymid - dc.parenthesis_length / 2,
            b.x1 + 2 * (b.x2 - b.x1),
            ymid + dc.parenthesis_length / 2,
            b.hx * 2,
            b.hy * dc.parenthesis_length / b.height,
            cut="right"
        )
