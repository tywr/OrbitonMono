import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph
from glyphs import Glyph
from draw.corner import draw_corner
from draw.rect import draw_rect


class LowercaseSGlyph(Glyph):
    name = "lowercase_s"
    unicode = "0x73"
    offset = 0
    width_ratio = 1
    stroke_x_ratio = 1.10
    stroke_y_ratio = 1.01
    right_tail_offset = 0.105
    left_tail_offset = 0.0525
    hx_ratio = 1
    hy_ratio = 1
    mid_height = 0.52
    opening1 = 0.28
    opening2 = 0.72
    thinning = 0.89
    left_offset = 0.08
    right_offset = 0.05

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_left=True,
            width_ratio=self.width_ratio,
        )
        sx, sy = self.stroke_x_ratio * dc.stroke_x, dc.stroke_y * self.stroke_y_ratio
        sa = dc.stroke_alt
        hx, hy = b.hx * self.hx_ratio, b.hy * self.hy_ratio
        yc1 = b.y1 + b.height * self.opening1
        yc2 = b.y1 + b.height * self.opening2
        ymid = b.y1 + self.mid_height * b.height
        x1 = b.x1 + self.left_offset * b.width
        x2 = b.x2 - self.right_offset * b.width
        hxt = (1 - self.left_offset - self.right_offset) * b.hx
        ym1 = (b.y2 + ymid - sy / 2) / 2
        ym2 = (b.y1 + ymid + sy / 2) / 2
        hyt, hyb = hy * (1 - self.mid_height), hy * (self.mid_height)

        draw_corner(
            pen,
            sx,
            sy,
            x1,
            ym1,
            b.xmid,
            b.y2,
            hxt,
            hy * (1 - self.mid_height),
            orientation="top-right",
        )

        # draw_corner(
        #     pen,
        #     sx,
        #     dc.stroke_alt,
        #     x1,
        #     (b.y2 + ymid - sy / 2) / 2,
        #     b.xmid,
        #     ymid - dc.stroke_alt / 2,
        #     hxt,
        #     hy * (1 - self.mid_height),
        #     orientation="bottom-right",
        # )
        # draw_corner(
        #     pen,
        #     sx,
        #     dc.stroke_alt,
        #     b.x2,
        #     (b.y1 + ymid + sy / 2) / 2,
        #     b.xmid,
        #     ymid + dc.stroke_alt / 2,
        #     hx,
        #     hy * self.mid_height,
        #     orientation="top-left",
        # )
        draw_corner(
            pen,
            sx,
            sy,
            b.x2,
            ym2,
            b.xmid,
            b.y1,
            hx,
            hy * self.mid_height,
            orientation="bottom-left",
        )

        # Mid Curve
        pen.moveTo((x1, ym1))
        pen.curveTo(
            (x1, b.ymid - sa / 2), (b.x2 - sx, b.ymid - sa / 2), (b.x2 - sx, ym2)
        )
        pen.lineTo((b.x2, ym2))
        pen.curveTo((b.x2, b.ymid + sa / 2), (x1 + sx, b.ymid + sa / 2), (x1 + sx, ym1))

        glyph = ufoLib2.objects.Glyph()
        draw_corner(
            glyph.getPen(),
            sx,
            sy,
            x2,
            (b.y2 + ymid - sy / 2) / 2,
            b.xmid,
            b.y2,
            hxt,
            hy * (1 - self.mid_height),
            orientation="top-left",
        )
        draw_corner(
            glyph.getPen(),
            sx * self.thinning,
            sy,
            b.x1,
            b.ymid,
            b.xmid,
            b.y1,
            hx,
            hy,
            orientation="bottom-right",
        )
        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(
            cut_glyph.getPen(),
            b.x1 - 10,
            yc1,
            b.x2 + 10,
            yc2,
        )
        res = BooleanGlyph(glyph).difference(BooleanGlyph(cut_glyph))
        res.draw(pen)
