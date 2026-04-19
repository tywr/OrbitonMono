from glyphs import Glyph
from draw.superellipse_arch import draw_superellipse_arch
from draw.rect import draw_rect
from draw.square_corner import draw_square_corner
from draw.corner import draw_corner
from draw.polygon import draw_polygon
from draw.parallelogramm import draw_smooth_parallelogramm_vertical


class LowercaseGGlyph(Glyph):
    name = "lowercase_g"
    unicode = "0x67"
    offset = -8
    tail_offset = 0
    bowl_stroke_x_ratio = 1.04
    bowl_stroke_y_ratio = 0.96
    tail_dip = 0.05
    tail_offset = 0.08

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

        # Bowl (open on the right, mirrored from b)
        arch_params = draw_superellipse_arch(
            pen,
            bsx,
            bsy,
            b.x1,
            b.y1,
            b.x2,
            b.y2,
            b.hx,
            b.hy,
            taper=dc.taper,
            side="right",
        )
        # Right stem with gap at baseline and dent inset
        draw_rect(pen, b.x2 - dc.stroke_x, 0, b.x2, dc.x_height)

        # Compute the intersection and fill the gap
        (_, y1), (_, y2) = arch_params["outer"].intersection_x(
            x=b.x2 - dc.stroke_x - dc.gap
        )
        y1, y2 = min(y1, y2), max(y1, y2)
        # draw_rect(pen, b.x2 - dc.stroke_x, y1, b.x2, y2)

        # Corner curving down-left into the descender
        draw_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x2,
            0,
            b.xmid,
            dc.descent + self.tail_offset,
            b.hx,
            b.hy,
            orientation="bottom-left",
        )

        draw_smooth_parallelogramm_vertical(
            pen,
            dc.stroke_y,
            b.xmid,
            dc.descent,
            b.x1 + self.tail_offset * b.width,
            dc.descent + self.tail_dip * b.height + dc.stroke_y,
            direction="top-left"
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
