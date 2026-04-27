from math import cos, sin
import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph
from glyphs import Glyph
from draw.rect import draw_rect
from draw.parallelogramm import draw_parallelogramm_vertical
from draw.polygon import draw_polygon


class LowercaseWGlyph(Glyph):
    name = "lowercase_w"
    unicode = "0x77"
    offset = 0
    overlap = 0.65
    overlap_middle = 0.5
    depth = 0.6
    inner_thickness_ratio = 1.5
    inner_height = 0.4
    width_ratio = 1.1
    ink_trap_height = 0.7

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            width_ratio=self.width_ratio,
            min_margin=dc.min_margin,
        )
        sx = dc.stroke_x
        delta = self.inner_thickness_ratio * dc.stroke_x
        yi = b.y2 - self.inner_height * b.height
        yik = b.y2 - self.ink_trap_height * b.height

        glyph = ufoLib2.objects.Glyph()
        gpen = glyph.getPen()

        # Vertical stems
        draw_rect(gpen, b.x1, b.y1, b.x1 + sx, b.y2)
        draw_rect(gpen, b.x2 - sx, b.y1, b.x2, b.y2)

        # Middle branches
        draw_parallelogramm_vertical(
            gpen,
            0,
            0,
            b.x1 + dc.stroke_x + dc.gap,
            b.y1,
            b.xmid - dc.gap / 2,
            yi + delta / 2,
            direction="top-right",
            delta=delta,
        )
        theta, _ = draw_parallelogramm_vertical(
            gpen,
            0,
            0,
            b.x2 - dc.stroke_x - dc.gap,
            b.y1,
            b.xmid + dc.gap / 2,
            yi + delta / 2,
            direction="top-left",
            delta=delta,
        )

        # Fill the gaps
        draw_rect(
            gpen,
            b.xmid - dc.gap / 2,
            yi - delta / 2,
            b.xmid + dc.gap / 2,
            yi,
        )
        draw_rect(
            gpen,
            b.x1 + sx,
            b.y1,
            b.x1 + sx + dc.gap,
            b.y1 + delta,
        )
        draw_rect(
            gpen,
            b.x2 - sx - dc.gap,
            b.y1,
            b.x2 - sx,
            b.y1 + delta,
        )

        cut_glyph = ufoLib2.objects.Glyph()

        # Cut the upper part, where the branches meet
        draw_rect(
            cut_glyph.getPen(),
            b.x1 + sx,
            yi,
            b.x2 - sx,
            yi + delta / 2,
        )

        le = max(0, (b.y1 + delta - yik) / cos(theta))
        if le > 0:
            draw_polygon(
                cut_glyph.getPen(),
                points=[
                    (b.x2 - sx - dc.gap, b.y1 + delta),
                    (
                        b.x2 - sx - dc.gap + le * sin(theta),
                        b.y1 + delta - le * cos(theta),
                    ),
                    (
                        b.x2 - sx + le * sin(theta),
                        b.y1 + delta - le * cos(theta),
                    ),
                    (b.x2 - sx, (b.y1 + b.y2 + delta) / 2),
                ],
            )
            draw_polygon(
                cut_glyph.getPen(),
                points=[
                    (b.x1 + sx + dc.gap, b.y1 + delta),
                    (
                        b.x1 + sx + dc.gap - le * sin(theta),
                        b.y1 + delta - le * cos(theta),
                    ),
                    (
                        b.x1 + sx - le * sin(theta),
                        b.y1 + delta - le * cos(theta),
                    ),
                    (b.x1 + sx, (b.y1 + b.y2 + delta) / 2),
                ],
            )

        res = BooleanGlyph(glyph).difference(BooleanGlyph(cut_glyph))
        res.draw(pen)
