import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph
from draw.rect import draw_rect
from draw.arch import draw_arch
from draw.polygon import draw_polygon
from draw.corner import draw_corner
from glyphs.lowercase.square import SquareLowercaseGlyph


class LowercaseY2Glyph(SquareLowercaseGlyph):
    name = "lowercase_y_2"
    unicode = "0x79"
    font_feature = {"cv02": 1}
    default_italic = True
    offset = 0

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
            width_ratio=self.width_ratio,
        )
        arch_top = b.y2
        tsx, tsy = (
            self.tail_stroke_x_ratio * dc.stroke_x,
            self.tail_stroke_y_ratio * dc.stroke_y,
        )
        xt = b.x1 + self.tail_offset * b.width

        # Bottom arch, cut at top (only lower half drawn)
        arch_params = draw_arch(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1,
            b.x2,
            arch_top,
            self.hx_ratio * b.hx,
            b.hy,
            taper=self.taper * dc.taper,
            side="right",
            cut="top",
        )

        # Compute the intersection of the outer bowl with the stem
        (_, y1), (_, y2) = arch_params["outer"].intersection_x(
            x=b.x2 - dc.stroke_x - dc.gap
        )
        y1, y2 = min(y1, y2), max(y1, y2)

        # Right stem — full x_height
        draw_rect(pen, b.x2 - dc.stroke_x, y1, b.x2, dc.x_height)

        draw_polygon(
            pen,
            points=[
                (b.x2 - dc.stroke_x, 0),
                (b.x2, 0),
                (b.x2, y1),
                (b.x2 - dc.stroke_x, y1),
            ],
        )

        # Fill the gap
        draw_polygon(
            pen,
            points=[
                (b.x2 - dc.stroke_x - dc.gap, y1),
                (b.x2 - dc.stroke_x, y1),
                (b.x2 - dc.stroke_x + dc.stroke_x * dc.taper * self.taper / 2, b.ymid),
            ],
        )

        # Left stem — starts from arch midpoint
        draw_rect(pen, b.x1, (arch_top + b.y1) / 2, b.x1 + dc.stroke_x, dc.x_height)

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
