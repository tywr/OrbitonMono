from glyphs import Glyph
from draw.parallelogramm import draw_parallelogramm


class ReverseSolidusGlyph(Glyph):
    name = "reverse_solidus"
    unicode = "0x5C"
    offset = 0
    width_ratio = 1
    height_ratio = 0.8

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="ascent", width_ratio=self.width_ratio
        )
        ymid = dc.parenthesis
        h = self.height_ratio * dc.parenthesis_length
        draw_parallelogramm(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x2,
            ymid - h / 2,
            b.x1,
            ymid + h / 2,
            direction="top-left"
        )
