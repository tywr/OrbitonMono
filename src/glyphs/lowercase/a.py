import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph
from config import FontConfig as fc
from glyphs import Glyph
from draw.superellipse_arch import draw_superellipse_arch
from draw.smooth_corner import draw_smooth_corner
from draw.corner import draw_corner
from draw.rect import draw_rect
from draw.polygon import draw_polygon
from draw.superellipse_loop import draw_superellipse_loop


class LowercaseAGlyph(Glyph):
    name = "lowercase_a"
    unicode = "0x61"
    offset = 0
    loop_ratio = 0.6
    width_ratio = 1
    stroke_x_ratio = 1.04
    stroke_y_ratio = 0.96
    taper = 0.15
    cap_hx_ratio = 1
    cap_hy_ratio = 0.8
    cap_ratio = 0.6
    cap_height = 0.75
    cap_width = 0.96
    thinning = 0.95

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_top=True,
            overshoot_bottom=True,
            overshoot_left=True,
            width_ratio=self.width_ratio,
        )
        sx, sy = self.stroke_x_ratio * dc.stroke_x, self.stroke_y_ratio * dc.stroke_y
        dx = sx - dc.stroke_x
        hx, hy = b.hx, b.hy * self.loop_ratio
        yc, ys = (
            b.y1 + self.cap_ratio * b.height,
            b.y1 + (2 * self.cap_ratio - 1) * b.height,
        )
        chx, chy = self.cap_hx_ratio * b.hx, self.cap_hy_ratio * b.hy
        ycut = self.cap_height * b.height
        cw, csx = self.cap_width * b.width, self.thinning * sx

        # Lower half half of the bowl
        arch_params = draw_superellipse_arch(
            pen,
            sx,
            sy,
            b.x1,
            b.y1,
            b.x2 + dx,
            b.y1 + b.height * self.loop_ratio,
            hx,
            hy,
            taper=self.taper,
            side="right",
            cut="top",
        )
        # Upper half of the bowl (corner + bar)
        draw_corner(
            pen,
            sx,
            dc.stroke_alt,
            b.x1,
            b.y1 + b.height * self.loop_ratio / 2,
            b.xmid,
            b.y1 + b.height * self.loop_ratio,
            hx,
            hy,
            orientation="top-right",
        )
        # Middle line
        draw_rect(
            pen,
            b.xmid,
            b.y1 + b.height * self.loop_ratio - dc.stroke_alt,
            b.x2 - dc.stroke_x,
            b.y1 + b.height * self.loop_ratio,
        )

        # Stem
        draw_rect(
            pen,
            b.x2 - sx,
            0,
            b.x2,
            yc,
        )
        draw_corner(
            pen, sx, sy, b.x2, yc, b.xmid, b.y2, chx, chy, orientation="top-left"
        )

        print(b.x2 - cw)
        loop_glyph = ufoLib2.objects.Glyph()
        draw_corner(
            loop_glyph.getPen(),
            csx,
            sy,
            b.x2 - cw,
            yc,
            b.xmid,
            b.y2,
            chx,
            chy,
            orientation="top-right"
        )
        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(cut_glyph.getPen(), b.x1, b.ymid, b.xmid, ycut)
        result = BooleanGlyph(loop_glyph).difference(BooleanGlyph(cut_glyph))
        result.draw(pen)

        # Fill the gap
        (_, y1), (_, y2) = arch_params["outer"].intersection_x(
            x=b.x2 - dc.stroke_x - dc.gap
        )
        y1, y2 = min(y1, y2), max(y1, y2)

        # Fill the gap
        draw_polygon(
            pen,
            points=[
                (b.x2 - dc.stroke_x - dc.gap, y1),
                (b.x2 - dc.stroke_x, y1),
                (b.x2 - dc.stroke_x + dc.stroke_x * dc.taper / 2, b.ymid),
            ],
        )
