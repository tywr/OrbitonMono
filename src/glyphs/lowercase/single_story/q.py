from draw.arch import draw_arch
from draw.rect import draw_rect
from draw.polygon import draw_polygon
from glyphs.lowercase.single_story import SingleStoryLowercaseGlyph


class LowercaseQGlyph(SingleStoryLowercaseGlyph):
    name = "lowercase_q"
    unicode = "0x71"
    offset = -10

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_left=True,
        )
        bsx, bsy = (
            self.bowl_stroke_x_ratio * dc.stroke_x,
            self.bowl_stroke_y_ratio * dc.stroke_y,
        )
        dx = bsx - dc.stroke_x
        hx, hy = self.hx_ratio * b.hx, self.hy_ratio * b.hy

        # Bowl (open on the right, same as d)
        arch_params = draw_arch(
            pen,
            bsx,
            bsy,
            b.x1,
            b.y1,
            b.x2 + dx,
            b.y2,
            hx,
            hy,
            taper=dc.taper,
            side="right",
        )
        # Compute the intersection of the outer bowl with the stem
        (_, y1), (_, y2) = arch_params["outer"].intersection_x(
            x=b.x2 - dc.stroke_x - dc.gap
        )
        y1, y2 = min(y1, y2), max(y1, y2)

        # Right descender stem
        draw_rect(pen, b.x2 - dc.stroke_x, dc.descent, b.x2, y2)
        draw_polygon(
            pen,
            points=[
                (b.x2 - dc.stroke_x, y2),
                (b.x2, y2),
                (b.x2, dc.x_height),
                (b.x2 - self.ending_thickness * dc.stroke_x, dc.x_height),
            ],
        )

        draw_polygon(
            pen,
            points=[
                (b.x2 - dc.stroke_x + dc.stroke_x * dc.taper / 2, b.ymid),
                (b.x2 - dc.stroke_x - dc.gap, y1),
                (b.x2 - dc.stroke_x, y1),
                (b.x2 - dc.stroke_x, y2),
                (b.x2 - dc.stroke_x - dc.gap, y2),
            ],
        )
