import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph

from glyphs.numbers import NumberGlyph
from draw.superellipse_arch import draw_superellipse_arch
from draw.superellipse_loop import draw_superellipse_loop
from draw.parallelogramm import draw_parallelogramm
from draw.rect import draw_rect
from utils.pens import NullPen


class FiveGlyph(NumberGlyph):
    name = "five"
    unicode = "0x35"
    offset = 0
    loop_ratio = 0.64
    junction_ratio = 0.42
    tilt = 0.25

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
        oj = self.tilt * b.width

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

        theta, delta = draw_parallelogramm(
            NullPen(),
            dc.stroke_x,
            dc.stroke_y,
            xj,
            yj,
            xj + oj,
            b.y2,
        )
        draw_parallelogramm(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            xj - delta,
            yj,
            xj + oj - delta,
            b.y2
        )
        draw_rect(
            pen, xj + oj - 2 * delta, b.y2 - dc.stroke_y, b.x2 - dc.h_overshoot, b.y2
        )
