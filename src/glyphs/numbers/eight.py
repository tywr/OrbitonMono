from glyphs.numbers import NumberGlyph
from draw.superellipse_arch import draw_superellipse_arch


class EightGlyph(NumberGlyph):
    name = "eight"
    unicode = "0x38"
    offset = 0
    height_ratio = 0.54
    loop_width_ratio = 0.92
    width_ratio = 1.03
    taper = 0.65

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_left=True,
            overshoot_right=True,
            width_ratio=self.width_ratio,
            number=True,
        )
        ymid = b.y1 + b.height * self.height_ratio
        wtop = self.loop_width_ratio * b.width
        dtop = (b.width - wtop) / 2

        # Top loop
        draw_superellipse_arch(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1 + dtop,
            ymid - dc.stroke_y / 2,
            b.x2 - dtop,
            b.y2,
            b.hx,
            b.hy * (1 - self.height_ratio),
            taper=self.taper,
            side="bottom",
        )

        # Bottom loop
        draw_superellipse_arch(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1,
            b.x2,
            ymid + dc.stroke_y / 2,
            b.hx,
            b.hy * self.height_ratio,
            taper=self.taper,
            side="top"
        )
