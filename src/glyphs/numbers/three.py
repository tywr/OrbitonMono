import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph

from glyphs.numbers import NumberGlyph
from draw.superellipse_arch import draw_superellipse_arch
from draw.rect import draw_rect


class ThreeGlyph(NumberGlyph):
    name = "three"
    unicode = "0x33"
    offset = 0
    width_ratio = 1.08
    taper = 0.6
    len_mid = 0.7

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_left=True,
            overshoot_right=True,
            width_ratio=self.width_ratio,
            number=True,
        )

        base_glyph = ufoLib2.objects.Glyph()
        ry = (b.y2 - b.ymid + dc.stroke_y / 2) / b.height

        # Top loop
        draw_superellipse_arch(
            base_glyph.getPen(),
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.ymid - dc.stroke_y / 2,
            b.x2,
            b.y2,
            b.hx,
            b.hy * ry,
            taper=self.taper,
            side="bottom",
        )

        # Bottom loop
        draw_superellipse_arch(
            base_glyph.getPen(),
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1,
            b.x2,
            b.ymid + dc.stroke_y / 2,
            b.hx,
            b.hy * ry,
            taper=self.taper,
            side="top",
        )

        # Remove the left-middle part
        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(
            cut_glyph.getPen(),
            b.x1,
            b.ymid - b.height / 4,
            b.x1 + b.width / 2,
            b.ymid + b.height / 4,
        )

        result = BooleanGlyph(base_glyph).difference(BooleanGlyph(cut_glyph))
        result.draw(pen)

        # Extension of the middle bar
        draw_rect(
            pen,
            b.x1 + (1 - self.len_mid) * b.width,
            b.ymid - dc.stroke_y / 2,
            b.xmid,
            b.ymid + dc.stroke_y / 2,
        )
