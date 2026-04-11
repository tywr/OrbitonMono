from glyphs.numbers import NumberGlyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.polygon import draw_polygon
from draw.parallelogramm import draw_parallelogramm_vertical


class ZeroGlyph(NumberGlyph):
    name = "zero"
    unicode = "0x30"
    offset = 0
    slash = 0.2

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            width_ratio=self.width_ratio,
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_left=True,
            overshoot_right=True,
            number=True,
        )

        draw_superellipse_loop(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1,
            b.x2,
            b.y2,
            b.hx,
            b.hy,
        )

        draw_parallelogramm_vertical(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1 + dc.stroke_x,
            b.y1 + dc.stroke_y,
            b.x2 - dc.stroke_x,
            b.y2 - dc.stroke_y,
        )
