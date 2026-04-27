import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph
from glyphs.uppercase import UppercaseGlyph
from draw.corner import draw_corner
from draw.rect import draw_rect


class UppercaseSGlyph(UppercaseGlyph):
    name = "uppercase_s"
    unicode = "0x53"
    offset = -10
    stroke_x_ratio = UppercaseGlyph.stroke_x_ratio * 1.00
    stroke_y_ratio = UppercaseGlyph.stroke_y_ratio * 1.05
    right_tail_offset = 0.01
    left_tail_offset = 0.01
    hx_ratio = 0.9
    hy_ratio = 0.8
    mid_height = 0.53
    opening1 = 0.28
    opening2 = 0.72
    thinning = 0.89
    left_offset = 0.08
    right_offset = 0.05
    width_ratio = 1.06
    curve_thinning = 0.028
    curve_ratio = 2.8

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_left=True,
            overshoot_right=True,
            height="cap",
            width_ratio=self.width_ratio,
            uppercase=True,
        )
        sx, sy = self.stroke_x_ratio * dc.stroke_x, dc.stroke_y * self.stroke_y_ratio
        hx, hy = b.hx * self.hx_ratio, b.hy * self.hy_ratio
        yc1 = b.y1 + b.height * self.opening1
        yc2 = b.y1 + b.height * self.opening2
        ymid = b.y1 + self.mid_height * b.height
        x1 = b.x1 + self.left_offset * b.width
        x2 = b.x2 - self.right_offset * b.width
        hxt = (1 - self.left_offset - self.right_offset) * b.hx
        ym1 = (b.y2 + ymid - sy / 2) / 2
        ym2 = (b.y1 + ymid + sy / 2) / 2
        th = self.curve_thinning * b.height
        r = self.curve_ratio

        thx, thy, tihx, tihy = draw_corner(
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
        bhx, bhy, bihx, bihy = draw_corner(
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
            (x1, ym1 - r * thy + th), (b.x2 - sx, ym2 + r * bihy + th), (b.x2 - sx, ym2)
        )
        pen.lineTo((b.x2, ym2))
        pen.curveTo(
            (b.x2, ym2 + r * bhy - th), (x1 + sx, ym1 - r * tihy - th), (x1 + sx, ym1)
        )

        # Endings
        glyph = ufoLib2.objects.Glyph()
        draw_corner(
            glyph.getPen(),
            sx * self.thinning,
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
            ym2,
            b.xmid,
            b.y1,
            hx,
            # hy,
            hy * self.mid_height,
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
