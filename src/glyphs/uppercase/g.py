import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph
from glyphs.uppercase import UppercaseGlyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.rect import draw_rect


class UppercaseGGlyph(UppercaseGlyph):
    name = "uppercase_g"
    unicode = "0x47"
    offset = 0
    opening = 140

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_left=True,
            overshoot_right=True,
            width_ratio=self.width_ratio,
            uppercase=True,
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio
        opening = self.opening * dc.cap / dc.x_height
        hx, hy = dc.hx * self.width_ratio, dc.hy * dc.cap / dc.x_height

        loop_glyph = ufoLib2.objects.Glyph()
        draw_superellipse_loop(
            loop_glyph.getPen(),
            sx,
            sy,
            b.x1,
            b.y1,
            b.x2,
            b.y2,
            hx,
            hy,
        )

        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(
            cut_glyph.getPen(),
            b.xmid,
            b.ymid,
            b.xmid + dc.window_width,
            b.ymid + opening - sy / 2,
        )

        result = BooleanGlyph(loop_glyph).difference(BooleanGlyph(cut_glyph))
        result.draw(pen)

        draw_rect(
            pen,
            b.xmid,
            b.ymid - sy,
            b.x2 - sx / 2,
            b.ymid,
        )
