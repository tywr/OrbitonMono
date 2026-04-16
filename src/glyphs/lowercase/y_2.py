from glyphs import Glyph
from draw.rect import draw_rect
from draw.square_corner import draw_square_corner
from draw.superellipse_arch import draw_superellipse_arch
from draw.polygon import draw_polygon


class LowercaseY2Glyph(Glyph):
    name = "lowercase_y_2"
    unicode = "0x79"
    font_feature = {"ss04": 1}
    default_italic = True
    offset = 0
    tail_offset = 0
    taper = 0.28
    hx_ratio = 1.15

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_left=True,
        )

        # Bowl (open on the right, mirrored from b)
        arch_params = draw_superellipse_arch(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1,
            b.x2,
            b.y2,
            self.hx_ratio * b.hx,
            b.hy,
            taper=self.taper,
            side="right",
            cut="top",
        )
        # Right stem with gap at baseline and dent inset
        draw_rect(pen, b.x2 - dc.stroke_x, 0, b.x2, dc.x_height)

        # Left stem - from arch midpoint
        draw_rect(pen, b.x1, b.ymid, b.x1 + dc.stroke_x, dc.x_height)

        # Compute the intersection and fill the gap
        (_, y1), (_, y2) = arch_params["outer"].intersection_x(
            x=b.x2 - dc.stroke_x - dc.gap
        )
        y1, y2 = min(y1, y2), max(y1, y2)

        # Fill the gap
        draw_polygon(
            pen,
            points=[
                (b.x2 - dc.stroke_x + dc.stroke_x * dc.taper / 2, b.ymid),
                (b.x2 - dc.stroke_x - dc.gap, y1),
                (b.x2 - dc.stroke_x, y1),
            ],
        )

        # Corner curving down-left into the descender
        draw_square_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x2,
            0,
            b.x2 - 0.8 * b.width,
            dc.descent + self.tail_offset,
            orientation="bottom-left",
        )
        # Horizontal tail along the descender
        draw_rect(
            pen,
            b.x1 + dc.stroke_x / 2,
            dc.descent + self.tail_offset,
            b.x2 - b.width / 2,
            dc.descent + self.tail_offset + dc.stroke_y,
        )
