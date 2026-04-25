import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph

from glyphs.numbers import NumberGlyph
from draw.arch import draw_arch
from draw.rect import draw_rect


class ThreeGlyph(NumberGlyph):
    name = "three"
    unicode = "0x33"
    offset = 0
    loop_width_ratio = 0.92
    mid_ratio = 0.53
    taper = 1.5
    len_mid = 0.7

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_right=True,
            width_ratio=self.width_ratio,
            number=True,
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio

        ymid = b.y1 + self.mid_ratio * b.height
        xl = b.x1 + (1 - self.loop_width_ratio) * b.width / 2
        xr = b.x2 - (1 - self.loop_width_ratio) * b.width / 2
        base_glyph = ufoLib2.objects.Glyph()
        ry = (b.y2 - b.ymid + sy / 2) / b.height

        # Top loop
        taper = max(self.taper * dc.taper, 0.65)
        top_params = draw_arch(
            base_glyph.getPen(),
            sx,
            sy,
            xl,
            ymid - sy / 2,
            xr,
            b.y2,
            b.hx,
            b.hy * ry * 2 * (1 - self.mid_ratio),
            taper=taper,
            side="bottom",
        )

        # Bottom loop
        bottom_params = draw_arch(
            base_glyph.getPen(),
            sx,
            sy,
            b.x1,
            b.y1,
            b.x2,
            ymid + sy / 2,
            b.hx,
            b.hy * ry * 2 * self.mid_ratio,
            taper=taper,
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
            ymid - sy / 2,
            intersection_x,
            ymid + sy / 2,
        )

        # Remove the left-middle part
        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(
            cut_glyph.getPen(),
            b.x1,
            ymid - b.height / 4,
            b.x1 + b.width / 2,
            ymid + b.height / 4,
        )

        result = BooleanGlyph(base_glyph).difference(BooleanGlyph(cut_glyph))
        result.draw(pen)

        # Extension of the middle bar
        draw_rect(
            pen,
            b.x1 + (1 - self.len_mid) * b.width,
            ymid - sy / 2,
            b.xmid,
            ymid + sy / 2,
        )
