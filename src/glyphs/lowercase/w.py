import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph
from math import tan, pi, sin, cos
from glyphs import Glyph
from draw.parallelogramm import draw_parallelogramm_vertical
from draw.rect import draw_rect


class LowercaseWGlyph(Glyph):
    name = "lowercase_w"
    unicode = "0x77"
    offset = 0
    width_ratio = 1.12
    inner_stroke_ratio = 0.94
    inner_thickness_ratio = 1.1
    inner_height_ratio = 1

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, width_ratio=self.width_ratio)
        yi = b.y1 + self.inner_height_ratio * b.height
        isx, isy = (
            self.inner_stroke_ratio * dc.stroke_x,
            self.inner_stroke_ratio * dc.stroke_y,
        )
        th = self.inner_thickness_ratio * dc.stroke_x

        draw_rect(
            pen,
            b.x1,
            b.y1,
            b.x1 + dc.stroke_x,
            b.y2,
        )
        draw_rect(
            pen,
            b.x2 - dc.stroke_x,
            b.y1,
            b.x2,
            b.y2,
        )

        glyph = ufoLib2.objects.Glyph()
        gpen = glyph.getPen()
        draw_parallelogramm_vertical(
            gpen,
            isx,
            isy,
            b.x1 + dc.stroke_x + dc.gap,
            b.y1,
            b.xmid + th / 2,
            yi,
        )
        theta, delta = draw_parallelogramm_vertical(
            gpen,
            isx,
            isy,
            b.x2 - dc.stroke_x - dc.gap,
            b.y1,
            b.xmid - th / 2,
            yi,
            direction="top-left",
        )
        h = tan(pi / 2 - theta) * th
        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(
            cut_glyph.getPen(),
            b.xmid - th / 2,
            yi - h,
            b.xmid + th / 2,
            yi,
        )
        res = BooleanGlyph(glyph).difference(BooleanGlyph(cut_glyph))
        res.draw(pen)

        draw_rect(
            pen, b.x1 + dc.stroke_x, b.y1, b.x1 + dc.stroke_x + dc.gap, b.y1 + delta
        )
        draw_rect(
            pen, b.x2 - dc.stroke_x - dc.gap, b.y1, b.x2 - dc.stroke_x, b.y1 + delta
        )
        draw_rect(
            pen,
            b.xmid - dc.gap / 2,
            yi - h / 2 - delta - 0.5 * dc.gap / tan(theta),
            b.xmid + dc.gap / 2,
            yi - h / 2 - delta,
        )

        # theta, delta = draw_parallelogramm(
        #     pen,
        #     dc.stroke_x,
        #     dc.stroke_y,
        #     b.xmid + self.inner_angle_ratio * b.width,
        #     0,
        #     b.x2,
        #     b.y2,
        # )
        # draw_parallelogramm(
        #     pen,
        #     dc.stroke_x,
        #     dc.stroke_y,
        #     b.xmid - self.inner_angle_ratio * b.width,
        #     0,
        #     b.x1,
        #     b.y2,
        #     direction="top-left",
        # )
        # theta2, delta2 = draw_parallelogramm(
        #     pen,
        #     isr * dc.stroke_x,
        #     isr * dc.stroke_y,
        #     b.xmid + self.inner_angle_ratio * b.width + ov,
        #     0,
        #     b.xmid - ovi,
        #     inner_height,
        #     direction="top-left",
        # )
        # draw_parallelogramm(
        #     pen,
        #     isr * dc.stroke_x,
        #     isr * dc.stroke_y,
        #     b.xmid - self.inner_angle_ratio * b.width - ov,
        #     0,
        #     b.xmid + ovi,
        #     inner_height,
        # )
        #
        # Fill the outer gaps
        # x = 1 / (1 + tan(theta) / tan(theta2))
        # p = x * (ov * tan(theta))
        # h = dc.gap * p / ov
        # draw_rect(
        #     pen,
        #     b.xmid + self.inner_angle_ratio * b.width - delta2 / 2,
        #     b.y1,
        #     b.xmid + self.inner_angle_ratio * b.width + ov,
        #     b.y1 + p + h,
        #     draw_rect(
        #         pen,
        #         b.xmid - self.inner_angle_ratio * b.width - ov,
        #         b.y1,
        #         b.xmid - self.inner_angle_ratio * b.width + delta2 / 2,
        #         b.y1 + p + h,
        #     ),
        # )

        # Fill the inside gap
        # h = dc.gap / (2 * tan(0.5 * pi - theta2))
        # p = ovi * tan(theta2)
        # draw_rect(
        #     pen,
        #     b.xmid - ovi,
        #     inner_height - p - h,
        #     b.xmid + ovi,
        #     inner_height,
        # )
