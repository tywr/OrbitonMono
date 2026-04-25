import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph
from glyphs.uppercase import UppercaseGlyph
from draw.rect import draw_rect
from draw.arch import draw_arch


class UppercaseGGlyph(UppercaseGlyph):
    name = "uppercase_g"
    unicode = "0x47"
    offset = 0
    opening = 140
    stroke_x_ratio = UppercaseGlyph.stroke_x_ratio * 1.05
    stroke_y_ratio = UppercaseGlyph.stroke_y_ratio * 1.1
    opening1 = 0.5
    opening2 = 0.72
    hy_ratio = 1
    hx_ratio = 1
    width_ratio = 1.12
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
            height="cap",
        )
        sx, sy = self.stroke_x_ratio * dc.stroke_x, self.stroke_y_ratio * dc.stroke_y
        hx, hy = self.hx_ratio * b.hx, self.hy_ratio * b.hy
        yc1 = b.y1 + b.height * self.opening1
        yc2 = b.y1 + b.height * self.opening2
        ymid = b.y1 + self.opening1 * b.height

        glyph = ufoLib2.objects.Glyph()
        draw_arch(
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

        draw_rect(
            pen,
            b.xmid,
            ymid - sy,
            b.x2 - sx / 2,
            ymid,
        )
