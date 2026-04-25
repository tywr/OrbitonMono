import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph
from draw.arch import draw_arch
from draw.rect import draw_rect
from draw.corner import draw_corner
from draw.polygon import draw_polygon
from glyphs.lowercase.single_story import SingleStoryLowercaseGlyph


class LowercaseGGlyph(SingleStoryLowercaseGlyph):
    name = "lowercase_g"
    unicode = "0x67"
    offset = -10

    tail_offset = 0
    tail_stroke_x_ratio = 0.89
    tail_stroke_y_ratio = 1.01
    tail_offset = 0.15
    cut_ratio = 0.25
    tail_offset = 0.02

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_left=True,
        )
        bsx, bsy = (
            self.bowl_stroke_x_ratio * dc.stroke_x,
            self.bowl_stroke_y_ratio * dc.stroke_y,
        )
        tsx, tsy = (
            self.tail_stroke_x_ratio * dc.stroke_x,
            self.tail_stroke_y_ratio * dc.stroke_y,
        )
        xt = b.x1 + self.tail_offset * b.width

        # Bowl (open on the right, mirrored from b)
        arch_params = draw_arch(
            pen,
            bsx,
            bsy,
            b.x1,
            b.y1,
            b.x2,
            b.y2,
            b.hx,
            b.hy,
            taper=dc.taper,
            side="right",
        )

        # Compute the intersection and fill the gap
        (_, y1), (_, y2) = arch_params["outer"].intersection_x(
            x=b.x2 - dc.stroke_x - dc.gap
        )
        y1, y2 = min(y1, y2), max(y1, y2)

        # Right stem with gap at baseline and dent inset
        draw_rect(pen, b.x2 - dc.stroke_x, 0, b.x2, y2)
        draw_polygon(
            pen,
            points=[
                (b.x2 - dc.stroke_x, y2),
                (b.x2, y2),
                (b.x2, dc.x_height),
                (b.x2 - self.ending_thickness * dc.stroke_x, dc.x_height),
            ],
        )

        # Corner curving down-left into the descender
        draw_corner(
            pen,
            dc.stroke_x,
            tsy,
            b.x2,
            0,
            b.xmid,
            dc.descent - dc.v_overshoot,
            b.hx,
            b.hy,
            orientation="bottom-left",
        )

        glyph = ufoLib2.objects.Glyph()
        draw_corner(
            glyph.getPen(),
            tsx,
            tsy,
            xt,
            0,
            b.xmid,
            dc.descent - dc.v_overshoot,
            b.hx,
            b.hy,
        )
        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(
            cut_glyph.getPen(),
            b.x1 - 10,
            dc.descent - dc.v_overshoot + b.height * self.cut_ratio,
            b.xmid,
            b.ymid,
        )
        res = BooleanGlyph(glyph).difference(BooleanGlyph(cut_glyph))
        res.draw(pen)

        draw_polygon(
            pen,
            points=[
                (b.x2 - dc.stroke_x + dc.stroke_x * dc.taper / 2, b.ymid),
                (b.x2 - dc.stroke_x - dc.gap, y1),
                (b.x2 - dc.stroke_x, y1),
                (b.x2 - dc.stroke_x, y2),
                (b.x2 - dc.stroke_x - dc.gap, y2),
            ],
        )
