import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph
from glyphs import Glyph
from draw.superellipse_arch import draw_superellipse_arch
from draw.corner import draw_corner
from draw.rect import draw_rect
from draw.polygon import draw_polygon


class LowercaseAGlyph(Glyph):
    name = "lowercase_a"
    unicode = "0x61"
    offset = -8
    mid_height = 0.52
    width_ratio = 1
    taper = 0.15
    cap_hx_ratio = 1.15
    cap_hy_ratio = 1
    cap_height = 0.72
    cap_offset = 0.01
    thinning = 0.89
    cap_stroke_x_ratio = 1.01
    cap_stroke_y_ratio = 1.1

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_top=True,
            overshoot_bottom=True,
            # overshoot_left=True,
            width_ratio=self.width_ratio,
        )
        sx, sy = dc.stroke_x, dc.stroke_y
        csx, csy = (
            self.cap_stroke_x_ratio * dc.stroke_x,
            self.cap_stroke_y_ratio * dc.stroke_y,
        )
        dx = sx - dc.stroke_x
        ry = (self.mid_height * b.height + dc.stroke_alt / 2) / b.height
        ymid = b.y1 + self.mid_height * b.height
        yl = ymid + dc.stroke_alt / 2
        hx, hy = b.hx, b.hy * ry
        ycut = b.y1 + self.cap_height * b.height
        xc = b.x1 + self.cap_offset * b.width
        chx = self.cap_hx_ratio * b.hx

        # Lower half half of the bowl
        arch_params = draw_superellipse_arch(
            pen,
            csx,
            csy,
            b.x1,
            b.y1,
            b.x2 + dx,
            yl,
            hx,
            hy,
            taper=self.taper,
            side="right",
            cut="top",
        )
        # Upper half of the bowl (corner + bar)
        draw_corner(
            pen,
            csx,
            dc.stroke_alt,
            b.x1,
            (b.y1 + yl) / 2,
            b.xmid,
            yl,
            hx,
            hy,
            orientation="top-right",
        )
        # Middle line
        draw_rect(
            pen,
            b.xmid,
            b.y1 + b.height * ry - dc.stroke_alt,
            b.x2 - dc.stroke_x,
            b.y1 + b.height * ry,
        )

        draw_corner(
            pen, sx, csy, b.x2, b.ymid, b.xmid, b.y2, chx, b.hy, orientation="top-left"
        )

        loop_glyph = ufoLib2.objects.Glyph()
        draw_corner(
            loop_glyph.getPen(),
            csx,
            csy,
            xc,
            b.ymid,
            b.xmid,
            b.y2,
            chx,
            b.hy,
            orientation="top-right",
        )
        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(cut_glyph.getPen(), b.x1, b.ymid, b.xmid, ycut)
        result = BooleanGlyph(loop_glyph).difference(BooleanGlyph(cut_glyph))
        result.draw(pen)

        # Stem
        draw_rect(
            pen,
            b.x2 - sx,
            0,
            b.x2,
            b.ymid,
        )

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
                (b.x2 - dc.stroke_x + dc.stroke_x * dc.taper / 2, ymid),
            ],
        )
