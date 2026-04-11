from glyphs.numbers import NumberGlyph
from draw.rect import draw_rect
from draw.superellipse_arch import draw_superellipse_arch
from draw.parallelogramm import draw_parallelogramm_vertical
from draw.cross_curve import draw_cross_curve_2
from draw.superellipse_loop import draw_superellipse_loop


class TwoGlyph(NumberGlyph):
    name = "two"
    unicode = "0x32"
    offset = 0
    width_ratio = 1.02

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_top=True,
            overshoot_right=True,
            overshoot_left=True,
            width_ratio=self.width_ratio,
            number=True,
        )

        # Top arch
        draw_superellipse_loop(
            pen,
            dc.stroke_x,
            dc.stroke_x,
            b.x1,
            b.ymid,
            b.x2,
            b.y2,
            b.hx,
            b.hy / 2,
            cut="bottom",
        )

        # Cross curve
        draw_cross_curve_2(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1 + dc.stroke_y,
            b.x2,
            b.y2 - b.height / 4,
            b.hx,
            b.hy / 3,
        )

        # Bottom bar
        draw_rect(pen, b.x1, 0, b.x2, dc.stroke_y)
