from glyphs.uppercase import UppercaseGlyph
from draw.superellipse_arch import draw_superellipse_arch
from draw.rect import draw_rect
import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph


class UppercaseCGlyph(UppercaseGlyph):
    name = "uppercase_c"
    unicode = "0x43"
    offset = 0
    stroke_x_ratio = UppercaseGlyph.stroke_x_ratio * 1.12
    stroke_y_ratio = UppercaseGlyph.stroke_y_ratio * 0.95
    opening1 = 0.3
    opening2 = 0.7
    hy_ratio = 1
    hx_ratio = 1
    width_ratio = 1.08
    thinning = 0.95

    def draw(self, pen, dc):

        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_left=True,
            overshoot_right=True,
            width_ratio=self.width_ratio,
            uppercase=True,
            height="cap"
        )
        sx, sy = self.stroke_x_ratio * dc.stroke_x, self.stroke_y_ratio * dc.stroke_y
        hx, hy = self.hx_ratio * b.hx, self.hy_ratio * b.hy
        yc1 = b.y1 + b.height * self.opening1
        yc2 = b.y1 + b.height * self.opening2

        glyph = ufoLib2.objects.Glyph()
        draw_superellipse_arch(
            glyph.getPen(),
            sx,
            sy,
            b.x1,
            b.y1,
            b.x2,
            b.y2,
            hx,
            hy,
            side="right",
            taper=self.thinning,
        )
        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(
            cut_glyph.getPen(),
            b.xmid,
            yc1,
            b.x2 + 10,
            yc2,
        )
        res = BooleanGlyph(glyph).difference(BooleanGlyph(cut_glyph))
        res.draw(pen)
