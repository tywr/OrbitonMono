from math import cos, sin
import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph
from glyphs.uppercase import UppercaseGlyph
from draw.rect import draw_rect
from draw.parallelogramm import draw_parallelogramm_vertical, draw_parallelogramm
from draw.polygon import draw_polygon


class UppercaseMGlyph(UppercaseGlyph):
    name = "uppercase_m"
    unicode = "0x4D"
    offset = 0
    overlap = 0.65
    overlap_middle = 0.5
    depth = 0.6
    inner_thickness_ratio = 2.6
    inner_height = 0.2
    width_ratio = 1.16
    ink_trap_height = 0.6

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            width_ratio=self.width_ratio,
            min_margin=dc.min_margin,
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio
        delta = self.inner_thickness_ratio * dc.stroke_x
        yi = b.y1 + self.inner_height * b.height
        yik = b.y1 + self.ink_trap_height * b.height

        # Vertical stems

        glyph = ufoLib2.objects.Glyph()
        gpen = glyph.getPen()
        draw_rect(gpen, b.x1, b.y1, b.x1 + sx, b.y2)
        draw_rect(gpen, b.x2 - sx, b.y1, b.x2, b.y2)
        draw_parallelogramm_vertical(
            gpen,
            0,
            0,
            b.x1 + dc.stroke_x + dc.gap,
            b.y2,
            b.xmid - dc.gap / 2,
            yi - delta / 2,
            direction="bottom-right",
            delta=delta,
        )
        theta, _ = draw_parallelogramm_vertical(
            gpen,
            0,
            0,
            b.x2 - dc.stroke_x - dc.gap,
            b.y2,
            b.xmid + dc.gap / 2,
            yi - delta / 2,
            direction="bottom-left",
            delta=delta,
        )
        draw_rect(
            gpen,
            b.xmid - dc.gap / 2,
            yi,
            b.xmid + dc.gap / 2,
            yi + delta / 2,
        )
        draw_rect(
            gpen,
            b.x1 + sx,
            b.y2 - delta,
            b.x1 + sx + dc.gap,
            b.y2,
        )
        draw_rect(
            gpen,
            b.x2 - sx - dc.gap,
            b.y2 - delta,
            b.x2 - sx,
            b.y2,
        )
        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(
            cut_glyph.getPen(),
            b.x1 + sx,
            yi - delta / 2,
            b.x2 - sx,
            yi,
        )
        le = max(0, (yik - b.y2 + delta) / cos(theta))
        if le > 0:
            draw_polygon(
                cut_glyph.getPen(),
                points=[
                    (b.x2 - sx - dc.gap, b.y2 - delta),
                    (
                        b.x2 - sx - dc.gap + le * sin(theta),
                        b.y2 - delta + le * cos(theta),
                    ),
                    (
                        b.x2 - sx + le * sin(theta) + dc.gap,
                        b.y2 - delta + le * cos(theta),
                    ),
                    (b.x2 - sx, (b.y1 + b.y2 - delta) / 2),
                ],
            )
            draw_polygon(
                cut_glyph.getPen(),
                points=[
                    (b.x1 + sx + dc.gap, b.y2 - delta),
                    (
                        b.x1 + sx + dc.gap - le * sin(theta),
                        b.y2 - delta + le * cos(theta),
                    ),
                    (
                        b.x1 + sx - le * sin(theta) - dc.gap,
                        b.y2 - delta + le * cos(theta),
                    ),
                    (b.x1 + sx, (b.y1 + b.y2 - delta) / 2),
                ],
            )

        res = BooleanGlyph(glyph).difference(BooleanGlyph(cut_glyph))
        res.draw(pen)

