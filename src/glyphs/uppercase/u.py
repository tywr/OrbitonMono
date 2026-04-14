from glyphs.uppercase import UppercaseGlyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.rect import draw_rect


class UppercaseUGlyph(UppercaseGlyph):
    name = "uppercase_u"
    unicode = "0x55"
    offset = 0

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_bottom=True,
            width_ratio=self.width_ratio,
            uppercase=True,
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio

        draw_superellipse_loop(
            pen, sx, sy, b.x1, b.y1, b.x2, b.y2, b.hx, b.hy, cut="top"
        )

        draw_rect(pen, b.x1, b.ymid, b.x1 + sx, b.y2)
        draw_rect(pen, b.x2 - sx, b.ymid, b.x2, b.y2)
