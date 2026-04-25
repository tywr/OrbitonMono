from glyphs.numbers import NumberGlyph
from draw.arch import draw_arch
from draw.rect import draw_rect


class EightGlyph(NumberGlyph):
    name = "eight"
    unicode = "0x38"
    offset = 0
    height_ratio = 0.53
    loop_width_ratio = 0.92
    taper = 1.5
    extra_overshoot = 0.000
    width_ratio = 1.06

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
        ymid = b.y1 + b.height * self.height_ratio
        wtop = self.loop_width_ratio * b.width
        dtop = (b.width - wtop) / 2
        ov = self.extra_overshoot * b.height

        # Top loop
        taper = max(self.taper * dc.taper, 0.65)
        top_params = draw_arch(
            pen,
            sx,
            sy,
            b.x1 + dtop,
            ymid - sy / 2,
            b.x2 - dtop,
            b.y2 + ov,
            b.hx,
            b.hy * (1 - self.height_ratio),
            taper=taper,
            side="bottom",
        )

        # Bottom loop
        bottom_params = draw_arch(
            pen,
            sx,
            sy,
            b.x1,
            b.y1 - ov,
            b.x2,
            ymid + sy / 2,
            b.hx,
            b.hy * self.height_ratio,
            taper=taper,
            side="top",
        )

        # Compute the intersection of the two outer superellipses
        # where there would be a dc.gap sized gap
        (xj1, _), (xj2, _) = top_params["outer"].intersection_superellipse(
            bottom_params["outer"].translate(dy=dc.gap)
        )
        draw_rect(
            pen,
            xj1,
            ymid - dc.gap,
            xj2,
            ymid + dc.gap,
        )
