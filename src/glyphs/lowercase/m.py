import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph

from glyphs import Glyph
from draw.arch import draw_arch
from draw.rect import draw_rect
from draw.polygon import draw_polygon


class LowercaseMGlyph(Glyph):
    name = "lowercase_m"
    unicode = "0x6D"
    offset = 0
    width_ratio = 1.18
    mid_len = 0.7
    top_stroke_y = 1
    hx_ratio = 0.82
    taper = 0.52
    ending_thickness = 0.75
    min_width = 70

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_top=True,
            width_ratio=self.width_ratio,
            min_margin=dc.min_margin,
        )
        mid_y = (1 - self.mid_len) * (b.height - b.y1)
        mid_offset = ((1 + self.taper * dc.taper) * dc.stroke_x - dc.gap) / 2
        hx, hy = b.hx * self.hx_ratio, b.hy

        # Left arch (x1 to xmid) and store offset_x

        glyph = ufoLib2.objects.Glyph()
        gpen = glyph.getPen()

        arch_params = draw_arch(
            gpen,
            dc.stroke_x,
            self.top_stroke_y * dc.stroke_y,
            b.x1,
            b.y1,
            b.xmid + mid_offset,
            b.y2,
            hx,
            hy,
            taper=self.taper * dc.taper,
            side="left",
            cut="m_junction",
        )

        # Right arch (xmid to x2)
        arch_params_2 = draw_arch(
            gpen,
            dc.stroke_x,
            self.top_stroke_y * dc.stroke_y,
            b.xmid - mid_offset,
            b.y1,
            b.x2,
            b.y2,
            hx,
            hy,
            taper=self.taper * dc.taper,
            side="left",
            cut="bottom",
        )

        # Compute the intersection and fill the gap
        (_, y1), (_, y2) = arch_params["outer"].intersection_x(x=b.x1 + dc.stroke_x)
        y1, y2 = min(y1, y2), max(y1, y2)

        # Left stem
        draw_rect(gpen, b.x1, 0, b.x1 + dc.stroke_x, y2)
        draw_polygon(
            gpen,
            points=[
                (b.x1 + self.ending_thickness * dc.stroke_x, dc.x_height),
                (b.x1, dc.x_height),
                (b.x1, y2),
                (b.x1 + dc.stroke_x - dc.gap, y2),
            ],
        )

        # Right foot — reaches up to the arch midpoint
        draw_rect(gpen, b.x2 - dc.stroke_x, 0, b.x2, b.ymid)

        # Middle stem extension
        draw_rect(
            gpen,
            b.xmid - (1 - self.taper * dc.taper) * dc.stroke_x / 2 - dc.gap / 2,
            mid_y,
            b.xmid + (1 - self.taper * dc.taper) * dc.stroke_x / 2 + dc.gap / 2,
            y2,
        )

        # We cut in the middle of the glyph in case it's not wide enough
        cut_glyph = ufoLib2.objects.Glyph()
        cpen = cut_glyph.getPen()

        se1 = arch_params["inner"]
        sew = se1.x2 - se1.x1
        sx = dc.stroke_x
        if sew < self.min_width:
            dx = self.min_width - sew
            xi1, yi1 = se1.xmid, se1.y2
            hx, hy = se1.hx, se1.hy
            se2 = arch_params_2["inner"]
            xi2, yi2 = se2.xmid, se2.y2
            # dhx = dx - hx

            cpen.moveTo((xi1, mid_y))
            cpen.lineTo((xi2, mid_y))
            cpen.lineTo((xi2, yi2))
            cpen.lineTo((xi2 - dx, yi2))
            cpen.curveTo(
                (xi2 - dx - hx, yi2),
                (b.xmid + sx / 2 - dx, b.ymid + hy),
                (b.xmid + sx / 2 - dx, b.ymid),
            )
            cpen.lineTo((b.xmid + sx / 2 - dx, mid_y))
            cpen.lineTo((b.xmid - sx / 2 + dx, mid_y))
            cpen.lineTo((b.xmid - sx / 2 + dx, b.ymid))
            cpen.curveTo(
                (b.xmid - sx / 2 + dx, b.ymid + hy),
                (xi1 + dx + hx, yi1),
                (xi1 + dx, yi1),
            )
            cpen.lineTo((xi1, yi1))
            cpen.closePath()

        res = BooleanGlyph(glyph).difference(BooleanGlyph(cut_glyph))
        res.draw(pen)
