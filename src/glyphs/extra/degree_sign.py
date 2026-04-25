from glyphs import Glyph
from draw.circle import draw_circle


class DegreeSignGlyph(Glyph):
    name = "degree_sign"
    unicode = "0xB0"
    offset = 0
    h_offset = 0.2
    width = 0.4
    stroke_ratio = 0.65
    width_ratio = 1

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            width_ratio=self.width_ratio,
        )
        s = self.stroke_ratio * dc.stroke_x
        w = self.width * b.width
        o = self.h_offset * b.height

        draw_circle(pen, b.xmid, b.y2 - o, w / 2 + s, clockwise=False)
        draw_circle(pen, b.xmid, b.y2 - o, w / 2, clockwise=True)
