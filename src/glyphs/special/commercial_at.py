from glyphs import Glyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.superellipse_arch import draw_superellipse_arch
from draw.rect import draw_rect


class CommercialAtGlyph(Glyph):
    name = "commercial_at"
    unicode = "0x40"
    offset = 0
    width_ratio = 1.08
    inner_ratio_x = 0.7
    inner_ratio_y = 0.5

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="cap", width_ratio=self.width_ratio
        )
        wi, hi = self.inner_ratio_x * b.width, self.inner_ratio_y * b.height
        xi1, xi2 = b.x2 - wi, b.x2
        yi1, yi2 = b.ymid - hi / 2, b.ymid + hi / 2

        draw_superellipse_arch(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            xi1,
            yi1,
            xi2,
            yi2,
            b.hx * self.inner_ratio_x,
            b.hy * self.inner_ratio_y,
            side="right",
            taper=dc.taper_a,
        )

        draw_superellipse_loop(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1,
            b.x2,
            b.y2,
            b.hx,
            b.hy,
            cut="bottom",
        )
        draw_superellipse_loop(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1,
            b.x2,
            b.y2,
            b.hx,
            b.hy,
            cut="right",
        )

        draw_rect(pen, b.xmid, b.y1, b.x2 - dc.stroke_x, b.y1 + dc.stroke_y)
        draw_rect(pen, b.x2 - dc.stroke_x, yi1, b.x2, b.ymid)
