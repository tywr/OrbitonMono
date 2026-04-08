import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph

from glyphs.numbers import NumberGlyph
from draw.superellipse_arch import draw_superellipse_arch
from draw.superellipse_loop import draw_superellipse_loop
from draw.rect import draw_rect


class FiveGlyph(NumberGlyph):
    name = "five"
    unicode = "0x35"
    offset = 0
    width_ratio = 1.1
    loop_ratio = 0.68
    junction_ratio = 0.43

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_bottom=True,
            overshoot_left=True,
            overshoot_right=True,
            width_ratio=self.width_ratio,
            number=True,
        )
        yj = b.y1 + b.height * self.junction_ratio

        base_glyph = ufoLib2.objects.Glyph()

        # Bottom loop
        params = draw_superellipse_loop(
            base_glyph.getPen(),
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1,
            b.x2,
            b.y1 + b.height * self.loop_ratio,
            b.hx,
            b.hy * self.loop_ratio,
            cut="top",
        )
        params = draw_superellipse_arch(
            base_glyph.getPen(),
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1,
            b.x2,
            b.y1 + b.height * self.loop_ratio,
            b.hx,
            b.hy * self.loop_ratio,
            taper=dc.taper,
            side="left",
            cut="bottom",
        )

        (x1, _), (x2, _) = params["inner"].intersection_y(y=yj)
        xj = min(x1, x2)

        # Remove the left-middle part
        cut_glyph = ufoLib2.objects.Glyph()
        ymid = b.y1 + b.height * self.loop_ratio / 2
        draw_rect(
            cut_glyph.getPen(),
            b.x1,
            2 * ymid - yj,
            b.xmid,
            yj,
        )

        result = BooleanGlyph(base_glyph).difference(BooleanGlyph(cut_glyph))
        result.draw(pen)

        draw_rect(pen, xj - dc.stroke_x, yj, xj, b.y2)
        draw_rect(
            pen, xj - dc.stroke_x, b.y2 - dc.stroke_y, b.x2 - dc.h_overshoot, b.y2
        )
