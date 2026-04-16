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
    hx_ratio = 0.78

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
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio

        base_glyph = ufoLib2.objects.Glyph()
        ry = (b.y2 - b.ymid + sy / 2) / b.height

        # Top loop
        top_params = draw_superellipse_arch(
            base_glyph.getPen(),
            sx,
            sy,
            b.x1,
            b.ymid - sy / 2,
            b.x2,
            b.y2,
            b.hx * self.hx_ratio,
            b.hy * ry,
            taper=self.taper,
            side="bottom",
        )

        # Bottom loop
        bottom_params = draw_superellipse_arch(
            base_glyph.getPen(),
            sx,
            sy,
            b.x1,
            b.y1,
            b.x2,
            b.ymid + sy / 2,
            b.hx * self.hx_ratio,
            b.hy * ry,
            taper=self.taper,
            side="top",
        )

        # Compute the intersection of the two outer superellipses
        # where there would be a dc.gap sized gap
        intersection_x = max(
            top_params["outer"].intersection_superellipse(
                bottom_params["outer"].translate(dy=dc.gap)
            ),
            key=lambda x: x[0],
        )[0]
        draw_rect(
            pen,
            b.xmid,
            b.ymid - sy / 2,
            intersection_x,
            b.ymid + sy / 2,
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
            b.ymid - sy / 2,
            b.xmid,
            b.ymid + sy / 2,
        )
