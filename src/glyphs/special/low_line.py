from glyphs import Glyph
from draw.rect import draw_rect


class LowLineGlyph(Glyph):
    name = "low_line"
    unicode = "0x5F"
    offset = 0
    stroke_ratio = 0.8
    width_ratio = 1

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="x_height", width_ratio=self.width_ratio
        )
        s = self.stroke_ratio * dc.stroke_x
        draw_rect(pen, b.x1, -s, b.x2, 0)
