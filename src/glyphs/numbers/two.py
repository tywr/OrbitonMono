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
    hx_ratio = 0.78

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_top=True,
            width_ratio=self.width_ratio,
            number=True,
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio

        # Top arch
        draw_superellipse_loop(
            pen,
            sx,
            sx,
            b.x1,
            b.ymid,
            b.x2,
            b.y2,
            b.hx * self.hx_ratio,
            b.hy / 2,
            cut="bottom",
        )

        # Cross curve
        draw_cross_curve_2(
            pen,
            sx,
            sy,
            b.x1,
            b.y1 + sy,
            b.x2,
            b.y2 - b.height / 4,
            b.hx,
            b.hy / 3,
        )

        # Bottom bar
        draw_rect(pen, b.x1, 0, b.x2, sy)
