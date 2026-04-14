from glyphs.uppercase import UppercaseGlyph
from draw.corner import draw_corner
from draw.rect import draw_rect


class UppercaseDGlyph(UppercaseGlyph):
    name = "uppercase_d"
    unicode = "0x44"
    offset = 0
    width_ratio=1.08

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_right=True,
            width_ratio=self.width_ratio,
            uppercase=True,
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio
        arch_x1 = b.x1
        cut_x = (arch_x1 + b.x2) / 2
        hx, hy = dc.hx * self.width_ratio, dc.hy * 0.5 * dc.cap / dc.x_height

        # Left stem
        draw_rect(pen, b.x1, 0, b.x1 + sx, dc.cap)
        # Right flat portion
        draw_rect(pen, b.x2 - sx, 0.5 * dc.cap, b.x2, 0.5 * dc.cap)
        # Connecting bars
        draw_rect(pen, b.x1, b.y2 - sy, cut_x, b.y2)
        draw_rect(pen, b.x1, 0, cut_x, sy)
        # Corner
        draw_corner(
            pen,
            sx,
            sy,
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
            sx,
            sy,
            b.x2,
            0.5 * dc.cap,
            cut_x,
            b.y1,
            hx,
            hy,
            orientation="bottom-left",
        )
