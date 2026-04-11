from glyphs.uppercase import UppercaseGlyph
from draw.corner import draw_corner
from draw.rect import draw_rect


class UppercaseDGlyph(UppercaseGlyph):
    name = "uppercase_d"
    unicode = "0x44"
    offset = 0

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_right=True,
            width_ratio=self.width_ratio,
        )
        arch_x1 = b.x1
        cut_x = (arch_x1 + b.x2) / 2
        hx, hy = dc.hx * self.width_ratio, dc.hy * 0.5 * dc.cap / dc.x_height

        # Left stem
        draw_rect(pen, b.x1, 0, b.x1 + dc.stroke_x, dc.cap)
        # Right flat portion
        draw_rect(pen, b.x2 - dc.stroke_x, 0.5 * dc.cap, b.x2, 0.5 * dc.cap)
        # Connecting bars
        draw_rect(pen, b.x1, b.y2 - dc.stroke_y, cut_x, b.y2)
        draw_rect(pen, b.x1, 0, cut_x, dc.stroke_y)
        # Corner
        draw_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x2,
            0.5 * dc.cap,
            cut_x,
            b.y2,
            hx,
            hy,
            orientation="top-left",
        )
        draw_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x2,
            0.5 * dc.cap,
            cut_x,
            b.y1,
            hx,
            hy,
            orientation="bottom-left",
        )
