import ufoLib2

from glyphs import Glyph
from draw.arch import draw_arch
from draw.rect import draw_rect


class LowercaseMGlyph(Glyph):
    name = "lowercase_m"
    unicode = "0x6D"
    offset = 0
    width_ratio = 1.16
    mid_len = 0.75
    top_stroke_y = 1
    hx_ratio = 0.75
    taper1 = 0.4
    taper2 = 0.8
    min_taper = 0.05
    min_taper_2 = 0.05
    ending_thickness = 0.75
    min_width = 74

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_top=True,
            width_ratio=self.width_ratio,
            min_margin=dc.min_margin_lowercase,
        )
        taper1 = max(self.min_taper, self.taper1 * dc.taper)
        taper2 = max(self.min_taper_2, self.taper2 * dc.taper)
        mid_y = (1 - self.mid_len) * (b.height - b.y1)
        hx, hy = b.hx * self.hx_ratio, b.hy

        wo = (b.width - 3 * dc.stroke_x) / 2
        if wo < self.min_width:
            smid = b.width - 2 * dc.stroke_x - 2 * self.min_width
        else:
            smid = dc.stroke_x
        mid_offset = smid / 2

        # Left arch (x1 to xmid) and store offset_x

        glyph = ufoLib2.objects.Glyph()

        draw_arch(
            pen,
            smid,
            self.top_stroke_y * dc.stroke_y,
            b.x1 + (dc.stroke_x - smid),
            b.y1,
            b.xmid + mid_offset,
            b.y2,
            hx,
            hy,
            taper=taper1,
            side="left",
            cut="bottom",
        )

        # Right arch (xmid to x2)
        draw_arch(
            pen,
            dc.stroke_x,
            self.top_stroke_y * dc.stroke_y,
            b.xmid - mid_offset - (dc.stroke_x - smid),
            b.y1,
            b.x2,
            b.y2,
            hx,
            hy,
            taper=taper2,
            side="left",
            cut="bottom",
        )

        # Left stem
        draw_rect(pen, b.x1, 0, b.x1 + dc.stroke_x, dc.x_height)

        # Right foot — reaches up to the arch midpoint
        draw_rect(pen, b.x2 - dc.stroke_x, 0, b.x2, b.ymid)

        # Middle stem extension
        draw_rect(
            pen,
            b.xmid - smid / 2,
            mid_y,
            b.xmid + smid / 2,
            b.ymid,
        )

        # We cut in the middle of the glyph in case it's not wide enough
        # cut_glyph = ufoLib2.objects.Glyph()
        # cpen = cut_glyph.getPen()
        #
        # se1 = arch_params["inner"]
        # sew = se1.x2 - se1.x1
        # sx = dc.stroke_x
        # if sew < self.min_width:
        #     dx = self.min_width - sew
        #     xi1, yi1 = se1.xmid, se1.y2
        #     hx, hy = se1.hx, se1.hy
        #     se2 = arch_params_2["inner"]
        #     xi2, yi2 = se2.xmid, se2.y2
        #     # dhx = dx - hx
        #
        #     cpen.moveTo((xi1, mid_y))
        #     cpen.lineTo((xi2, mid_y))
        #     cpen.lineTo((xi2, yi2))
        #     cpen.lineTo((xi2 - dx, yi2))
        #     cpen.curveTo(
        #         (xi2 - dx - hx, yi2),
        #         (b.xmid + sx / 2 - dx, b.ymid + hy),
        #         (b.xmid + sx / 2 - dx, b.ymid),
        #     )
        #     cpen.lineTo((b.xmid + sx / 2 - dx, mid_y))
        #     cpen.lineTo((b.xmid - sx / 2 + dx, mid_y))
        #     cpen.lineTo((b.xmid - sx / 2 + dx, b.ymid))
        #     cpen.curveTo(
        #         (b.xmid - sx / 2 + dx, b.ymid + hy),
        #         (xi1 + dx + hx, yi1),
        #         (xi1 + dx, yi1),
        #     )
        #     cpen.lineTo((xi1, yi1))
        #     cpen.closePath()
        #
        # res = BooleanGlyph(glyph).difference(BooleanGlyph(cut_glyph))
        # res.draw(pen)
