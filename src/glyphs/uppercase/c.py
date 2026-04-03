import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph
from glyph import Glyph
from shapes.superellipse_loop import draw_superellipse_loop
from shapes.rect import draw_rect


class UppercaseCGlyph(Glyph):
    name = "uppercase_c"
    unicode = "0x43"
    offset = 0
    width_ratio = 350 / 340
    opening = 280  # Opening height at x_height, scaled to ascent in draw

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="ascent",
            width_ratio=self.width_ratio,
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_left=True,
            overshoot_right=True,
        )
        hy = dc.hy * dc.ascent / dc.x_height  # Scale hy to cap height
        opening = self.opening * dc.ascent / dc.x_height

        loop_glyph = ufoLib2.objects.Glyph()
        draw_superellipse_loop(loop_glyph.getPen(), dc.stroke, b.x1, b.y1, b.x2, b.y2, dc.hx, hy)

        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(
            cut_glyph.getPen(),
            b.xmid,
            b.ymid - opening / 2 + dc.stroke / 2,
            b.xmid + dc.window_width,
            b.ymid + opening / 2 - dc.stroke / 2,
        )

        result = BooleanGlyph(loop_glyph).difference(BooleanGlyph(cut_glyph))
        result.draw(pen)
