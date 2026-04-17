from glyphs import Glyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.corner import draw_corner
from draw.rect import draw_rect
import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph


class LowercaseEGlyph(Glyph):
    name = "lowercase_e"
    unicode = "0x65"
    offset = 0
    width_ratio = 1
    stroke_x_ratio = 1.00
    stroke_y_ratio = 0.96
    tail_height = 0.25
    mid_height = 0.52
    thinning = 0.9
    stroke_x_ratio = 1.04
    stroke_y_ratio = 0.96

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_top=True,
            overshoot_left=True,
            overshoot_right=True,
            width_ratio=self.width_ratio,
        )
        sx, sy = self.stroke_x_ratio * dc.stroke_x, self.stroke_y_ratio * dc.stroke_y
        hx, hy = b.hx * (b.width - dc.h_overshoot) / b.width, b.hy
        yo = self.tail_height * b.height
        ymid = self.mid_height * b.height

        # Half-top of a superellipse
        draw_superellipse_loop(
            pen,
            sx,
            sy,
            b.x1,
            b.y1,
            b.x2,
            b.y2,
            b.hx,
            b.hy,
            cut="right",
        )

        loop_glyph = ufoLib2.objects.Glyph()
        draw_corner(
            loop_glyph.getPen(),
            sx * self.thinning,
            sy,
            b.x2,
            b.ymid,
            b.xmid,
            b.y1,
            b.hx,
            b.hy,
            orientation="bottom-left",
        )

        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(
            cut_glyph.getPen(),
            b.xmid,
            yo,
            b.xmid + b.width,
            b.ymid,
        )
        result = BooleanGlyph(loop_glyph).difference(BooleanGlyph(cut_glyph))
        result.draw(pen)

        draw_corner(
            pen,
            sx,
            sy,
            b.x2 - dc.h_overshoot,
            ymid,
            b.xmid,
            b.y2,
            hx,
            hy,
            orientation="top-left",
        )
        draw_rect(
            pen,
            b.x1 + sx / 2,
            ymid,
            b.x2 - dc.h_overshoot - sx / 2,
            ymid + dc.stroke_alt / 2,
        )
        draw_rect(
            pen, b.x1 + sx / 2, ymid - dc.stroke_alt / 2, b.x2 - dc.h_overshoot, ymid
        )
