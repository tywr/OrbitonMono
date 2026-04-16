from glyphs import Glyph
from draw.superellipse_arch import draw_superellipse_arch
from draw.rect import draw_rect
from draw.polygon import draw_polygon
from draw.corner import draw_corner


class LowercaseA3Glyph(Glyph):
    name = "lowercase_a_3"
    unicode = "0x61"
    font_feature = {"ss01": 2}
    offset = 0
    loop_ratio = 0.6
    width_ratio = 1

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_left=True,
            width_ratio=self.width_ratio,
        )
        hx, hy = b.hx, b.hy * self.loop_ratio

        # Lower half half of the bowl
        arch_params = draw_superellipse_arch(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1,
            b.x2,
            b.y1 + b.height * self.loop_ratio,
            hx,
            hy,
            taper=dc.taper_a,
            side="right",
        )

        # Curve to the cap
        draw_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x2,
            b.y1 + b.height / 2,
            b.xmid,
            b.y2,
            dc.hy,
            dc.hy,
            orientation="top-left",
        )
        # Cap
        draw_rect(
            pen,
            b.x1 + dc.stroke_x / 2,
            dc.x_height - dc.stroke_y,
            b.xmid,
            dc.x_height,
        )

        # Stem
        draw_rect(
            pen,
            b.x2 - dc.stroke_x,
            0,
            b.x2,
            b.y1 + b.height / 2,
        )

        # Fill the gap
        (_, y1), (_, y2) = arch_params["outer"].intersection_x(x=b.x2 - dc.stroke_x - dc.gap)
        y1, y2 = min(y1, y2), max(y1, y2)

        # Fill the gap
        draw_polygon(
            pen,
            points=[
                (b.x2 - dc.stroke_x - dc.gap, y1),
                (b.x2 - dc.stroke_x, y1),
                (b.x2 - dc.stroke_x + dc.stroke_x * dc.taper / 2, b.ymid),
                (b.x2 - dc.stroke_x, y2),
                (b.x2 - dc.stroke_x - dc.gap, y2),
            ],
        )

        # draw_rect(
        #     pen,
        #     b.x2 - dc.stroke_x,
        #     y1,
        #     b.x2,
        #     b.y1 + b.height / 2,
        # )
