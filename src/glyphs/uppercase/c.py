from glyphs.uppercase import UppercaseGlyph
from draw.loop import draw_loop
from draw.corner import draw_corner
from draw.rect import draw_rect
import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph


class UppercaseCGlyph(UppercaseGlyph):
    name = "uppercase_c"
    unicode = "0x43"
    offset = 0
    stroke_x_ratio = UppercaseGlyph.stroke_x_ratio * 1.00
    stroke_y_ratio = UppercaseGlyph.stroke_y_ratio * 1.00
    opening1 = 0.28
    opening2 = 0.72
    thinning = 0.95
    top_offset = 0.02
    width_ratio = 1.08

    def draw(self, pen, dc):

        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            height="cap",
            width_ratio=self.width_ratio,
            uppercase=True,
        )
        sx, sy = self.stroke_x_ratio * dc.stroke_x, self.stroke_y_ratio * dc.stroke_y
        yc1 = b.y1 + b.height * self.opening1
        yc2 = b.y1 + b.height * self.opening2
        xt = b.x2 - self.top_offset * b.width

        draw_loop(pen, sx, sy, b.x1, b.y1, b.x2, b.y2, b.hx, b.hy, cut="right")

        glyph = ufoLib2.objects.Glyph()
        draw_corner(
            glyph.getPen(),
            sx * self.thinning,
            sy,
            xt,
            b.ymid,
            b.xmid,
            b.y2,
            b.hx,
            b.hy,
            orientation="top-left",
        )
        draw_corner(
            glyph.getPen(),
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
            yc1,
            b.x2 + 10,
            yc2,
        )
        res = BooleanGlyph(glyph).difference(BooleanGlyph(cut_glyph))
        res.draw(pen)
