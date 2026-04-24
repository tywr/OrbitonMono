from glyphs import Glyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.corner import draw_corner
from draw.rect import draw_rect
import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph


class LowercaseEGlyph(Glyph):
    name = "lowercase_e"
    unicode = "0x65"
    offset = 5
    width_ratio = 1
    mid_height = 0.52
    stroke_x_ratio = 1.01
    stroke_y_ratio = 1.10
    thinning = 0.89
    tail_offset = 0.01
    tail_height = 0.28

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_top=True,
            overshoot_left=True,
            overshoot_right=True,
            overshoot_bottom=True,
            width_ratio=self.width_ratio,
        )
        sx, sy = self.stroke_x_ratio * dc.stroke_x, self.stroke_y_ratio * dc.stroke_y
        yo = b.y1 + self.tail_height * b.height
        ymid = b.y1 + self.mid_height * b.height
        xt = b.x2 + self.tail_offset * b.width

        # Half-left as the o-shape
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

        # Top-right corner
        draw_corner(
            pen,
            sx,
            sy,
            b.x2 - dc.h_overshoot,
            b.ymid,
            b.xmid,
            b.y2,
            b.hx,
            b.hy,
            orientation="top-left",
        )

        loop_glyph = ufoLib2.objects.Glyph()
        draw_corner(
            loop_glyph.getPen(),
            sx * self.thinning,
            sy,
            xt,
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

        draw_rect(
            pen,
            b.x1 + sx / 2,
            ymid,
            b.x2 - dc.h_overshoot - sx / 2,
            ymid + dc.stroke_alt / 2,
        )
        draw_rect(
            pen, b.x1 + sx / 2, ymid - dc.stroke_alt / 2, b.x2 - dc.h_overshoot, max(ymid, b.ymid)
        )
