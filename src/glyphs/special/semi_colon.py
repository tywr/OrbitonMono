from glyphs import Glyph
from glyphs.special.comma import CommaGlyph
from draw.rect import draw_rect
from draw.polygon import draw_polygon


class SemiColonGlyph(Glyph):
    name = "semi_colon"
    unicode = "0x3B"
    offset = 0
    width_ratio = 1
    stroke_ratio = 1.5
    gap = 1

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="x_height", width_ratio=self.width_ratio
        )
        s = self.stroke_ratio * dc.stroke_x
        g = b.height * self.gap

        draw_rect(
            pen,
            b.xmid - s / 2,
            b.y1 + g - s,
            b.xmid + s / 2,
            b.y1 + g,
        )
        cg = CommaGlyph()
        cg.draw(pen, dc)
