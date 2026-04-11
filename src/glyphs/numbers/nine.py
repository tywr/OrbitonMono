import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph

from glyphs.numbers import NumberGlyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.superellipse_arch import draw_superellipse_arch
from draw.rect import draw_rect
from draw.corner import draw_corner


class NineGlyph(NumberGlyph):
    name = "nine"
    unicode = "0x39"
    offset = 0
    vertical_ratio = 0.6
    bottom_cut = 0.2

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_top=True,
            overshoot_left=True,
            overshoot_right=True,
            overshoot_bottom=True,
            width_ratio=self.width_ratio,
            number=True,
        )

        ymid = b.y2 - self.vertical_ratio * b.height
        ycut = b.y1 + self.bottom_cut * b.height

        # Upper loop
        draw_superellipse_arch(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            ymid,
            b.x2,
            b.y2,
            b.hx,
            b.hy * self.vertical_ratio,
            taper=dc.taper,
            side="right",
            cut="top",
        )
        draw_superellipse_loop(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            ymid,
            b.x2,
            b.y2,
            b.hx,
            b.hy * self.vertical_ratio,
            cut="bottom",
        )
        draw_rect(pen, b.x2 - dc.stroke_x, b.ymid, b.x2, b.y2 - (b.y2 - ymid) / 2)

        loop_glyph = ufoLib2.objects.Glyph()
        draw_superellipse_loop(
            loop_glyph.getPen(),
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1,
            b.x2,
            b.y2,
            b.hx,
            b.hy,
            cut="top"
        )

        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(cut_glyph.getPen(), b.x1, ycut, b.xmid, b.y2)

        result = BooleanGlyph(loop_glyph).difference(BooleanGlyph(cut_glyph))
        result.draw(pen)
