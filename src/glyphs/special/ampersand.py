from math import tan
import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph

from glyphs import Glyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.superellipse_arch import draw_superellipse_arch
from draw.rect import draw_rect
from draw.parallelogramm import draw_parallelogramm
from utils.pens import NullPen


class AmpersandGlyph(Glyph):
    name = "ampersand"
    unicode = "0x26"
    offset = -50
    width_ratio = 1.08
    upper_width = 0.8
    upper_height = 0.4
    lower_width = 1
    hook_ratio = 0.12
    hook_below_baseline = 0
    hook_outside_cell = 0.24
    end_height_ratio = 0.5

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_top=True,
            overshoot_bottom=True,
            width_ratio=self.width_ratio,
        )

        ox = self.hook_outside_cell * b.width
        h = self.upper_height * b.height
        w = self.upper_width * b.width
        xu1, xu2 = b.xmid - w / 2, b.xmid + w / 2
        yu1, yu2 = b.y2 - h, b.y2
        hux, huy = b.hx * w / b.width, b.hy * h / b.height

        params = draw_superellipse_loop(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            xu1,
            yu1,
            xu2,
            yu2,
            hux,
            huy,
            cut="bottom",
        )

        xj = xu1 + self.hook_ratio * w
        (_, y1), (_, y2) = params["outer"].intersection_x(x=xj)
        yj = min(y1, y2)

        # Draw the parallelogramm to the bottom right
        dhy = self.hook_below_baseline * b.height
        theta, delta = draw_parallelogramm(
            NullPen(),
            dc.stroke_x,
            dc.stroke_y,
            b.x2 + ox,
            -dhy,
            xj,
            yj,
            direction="top-left",
        )

        # Draw the curve to the intersection
        hy = (0.5 * yu1 + 0.5 * yu2 - yj) - tan(theta) * (xj - xu1)
        pen.moveTo((xu1, 0.5 * yu1 + 0.5 * yu2))
        pen.curveTo(
            (xu1, 0.5 * yu1 + 0.5 * yu2 - hy),
            (xj, yj),
            # (xj, yj),
            (b.x2 + ox - delta, -dhy),
        )
        pen.lineTo((b.x2 + ox, -dhy))
        pen.curveTo(
            (xj + delta, yj),
            (xu1 + dc.stroke_x, 0.5 * yu1 + 0.5 * yu2 - hy),
            (xu1 + dc.stroke_x, 0.5 * yu1 + 0.5 * yu2),
        )
        pen.closePath()

        # Draw the lower bowl
        xbm = b.xmid
        lw = self.lower_width * b.width
        lh = yj - b.y1

        draw_superellipse_arch(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            xbm - lw / 2,
            b.y1,
            xbm + lw / 2,
            yj,
            b.hx * lw / b.width,
            b.hy * lh / b.height,
            cut="top",
            side="top",
            taper=0.5,
        )

        loop_glyph = ufoLib2.objects.Glyph()
        draw_superellipse_arch(
            loop_glyph.getPen(),
            dc.stroke_x,
            dc.stroke_y,
            xbm - lw / 2,
            b.y1,
            xbm + lw / 2,
            yj,
            b.hx * lw / b.width,
            b.hy * lh / b.height,
            cut="right",
            side="top",
            taper=0.5,
        )

        xcut = xj + delta
        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(cut_glyph.getPen(), xcut, 0.5 * b.y1 + 0.5 * yj, b.x2, b.y2)
        result = BooleanGlyph(loop_glyph).difference(BooleanGlyph(cut_glyph))
        result.draw(pen)

        # Draw the height extension
        eh = self.end_height_ratio * b.height
        draw_rect(
            pen, xbm + lw / 2 - dc.stroke_x, 0.5 * b.y1 + 0.5 * yj, xbm + lw / 2, eh
        )
