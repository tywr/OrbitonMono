from glyphs import Glyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.arch import draw_arch
from draw.rect import draw_rect
from draw.polygon import draw_polygon
from draw.corner import draw_corner


class CommercialAtGlyph(Glyph):
    name = "commercial_at"
    unicode = "0x40"
    offset = 0
    width_ratio = 1.22
    inner_ratio_x = 0.65
    inner_ratio_y = 0.45
    ending_thickness = 0.8

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_top=True,
            overshoot_left=True,
            overshoot_right=True,
            width_ratio=self.width_ratio,
        )
        wi, hi = self.inner_ratio_x * b.width, self.inner_ratio_y * b.height
        xi1, xi2 = b.x2 - wi, b.x2
        yi1, yi2 = b.ymid - hi / 2, b.ymid + hi / 2

        params = draw_arch(
            pen,
            dc.stroke_x,
            dc.stroke_alt,
            xi1,
            yi1,
            xi2,
            yi2,
            b.hx * self.inner_ratio_x,
            b.hy * self.inner_ratio_y,
            side="right",
            taper=0.2,
        )

        # Compute the intersection and fill the gap
        (_, y1), (_, y2) = params["outer"].intersection_x(
            x=b.x2 - dc.stroke_x - dc.gap
        )
        y1, y2 = min(y1, y2), max(y1, y2)

        draw_polygon(
            pen,
            points=[
                (b.x2 - self.ending_thickness * dc.stroke_x, yi1),
                (b.x2, yi1),
                (b.x2, y1),
                (b.x2 - dc.stroke_x, y1),
            ],
        )

        draw_polygon(
            pen,
            points=[
                (b.x2 - dc.stroke_x + dc.stroke_x * dc.taper / 4, b.ymid),
                (b.x2 - dc.stroke_x - dc.gap, y1),
                (b.x2 - dc.stroke_x, y1),
                (b.x2 - dc.stroke_x, y2),
                (b.x2 - dc.stroke_x - dc.gap, y2),
            ],
        )

        # draw_superellipse_loop(
        #     pen,
        #     dc.stroke_x,
        #     dc.stroke_y,
        #     b.x1,
        #     b.y1,
        #     b.x2,
        #     b.y2,
        #     b.hx,
        #     b.hy,
        #     cut="bottom",
        # )
        draw_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x2,
            b.ymid,
            b.xmid,
            b.y2,
            b.hx,
            b.hy,
            orientation="top-left"
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

        draw_rect(pen, b.x2 - dc.stroke_x, y1, b.x2, b.ymid)
        draw_rect(pen, b.xmid, b.y1, b.x2 - dc.stroke_x, b.y1 + dc.stroke_y)
