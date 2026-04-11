import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph

from glyphs.numbers import NumberGlyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.superellipse_arch import draw_superellipse_arch
from draw.rect import draw_rect
from draw.corner import draw_corner


class SixGlyph(NumberGlyph):
    name = "six"
    unicode = "0x36"
    offset = 0
    loop_ratio = 0.6
    top_ratio = 0.4
    top_cut = 0.8

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_bottom=True,
            overshoot_left=True,
            overshoot_right=True,
            overshoot_top=True,
            width_ratio=self.width_ratio,
            number=True,
        )

        ymid = b.y1 + self.loop_ratio * b.height
        ytop = b.y1 + self.top_ratio * b.height
        ycut = b.y1 + self.top_cut * b.height

        # Bottom loop
        draw_superellipse_arch(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1,
            b.x2,
            ymid,
            b.hx,
            b.hy * self.loop_ratio,
            taper=dc.taper,
            side="left",
            cut="bottom",
        )
        draw_superellipse_loop(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1,
            b.x2,
            ymid,
            b.hx,
            b.hy * self.loop_ratio,
            cut="top",
        )
        draw_rect(
            pen,
            b.x1,
            b.y1 + (ymid - b.y1) / 2,
            b.x1 + dc.stroke_x,
            b.ymid,
        )
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
            cut="bottom"
        )

        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(cut_glyph.getPen(), b.xmid, b.y1, b.x2, ycut)

        result = BooleanGlyph(loop_glyph).difference(BooleanGlyph(cut_glyph))
        result.draw(pen)
