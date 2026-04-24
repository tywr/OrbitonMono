from glyphs import Glyph
from draw.superellipse_arch import draw_superellipse_arch
from draw.rect import draw_rect
from draw.polygon import draw_polygon


class LowercasePGlyph(Glyph):
    name = "lowercase_p"
    unicode = "0x70"
    offset = 10
    bowl_stroke_x_ratio = 1.1
    bowl_stroke_y_ratio = 1.01
    ending_thickness = 0.8
    hx_ratio = 1.03
    hy_ratio = 1

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_right=True,
        )
        bsx, bsy = (
            self.bowl_stroke_x_ratio * dc.stroke_x,
            self.bowl_stroke_y_ratio * dc.stroke_y,
        )
        dx = bsx - dc.stroke_x
        hx, hy = self.hx_ratio * b.hx, self.hy_ratio * b.hy

        # Bowl (open on the left, same as b)
        arch_params = draw_superellipse_arch(
            pen,
            bsx,
            bsy,
            b.x1 - dx,
            b.y1,
            b.x2,
            b.y2,
            hx,
            hy,
            taper=dc.taper,
            side="left",
        )

        # Compute the intersection of the outer bowl with the stem
        (_, y1), (_, y2) = arch_params["outer"].intersection_x(
            x=b.x1 + dc.stroke_x + dc.gap
        )
        y1, y2 = min(y1, y2), max(y1, y2)

        # Left descender stem
        draw_rect(pen, b.x1, dc.descent, b.x1 + dc.stroke_x, y2)
        draw_polygon(
            pen,
            points=[
                (b.x1 + self.ending_thickness * dc.stroke_x, dc.x_height),
                (b.x1, dc.x_height),
                (b.x1, y2),
                (b.x1 + dc.stroke_x, y2),
            ],
        )

        draw_polygon(
            pen,
            points=[
                (b.x1 + dc.stroke_x + dc.gap, y2),
                (b.x1 + dc.stroke_x, y2),
                (b.x1 + dc.stroke_x, y1),
                (b.x1 + dc.stroke_x + dc.gap, y1),
                (b.x1 + dc.stroke_x - dc.stroke_x * dc.taper / 2, b.ymid),
            ],
        )
