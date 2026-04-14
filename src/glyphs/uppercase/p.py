from glyphs.uppercase import UppercaseGlyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.rect import draw_rect


class UppercasePGlyph(UppercaseGlyph):
    name = "uppercase_p"
    unicode = "0x50"
    offset = 8
    loop_ratio = 0.6

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_right=True,
            width_ratio=self.width_ratio,
            uppercase=True,
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio
        hx, hy = b.hx, b.hy * self.loop_ratio
        ymid = b.y1 + (1 - self.loop_ratio) * b.height

        # Left stem
        draw_rect(pen, b.x1, 0, b.x1 + sx, dc.cap)

        # Upper loop (narrower, displaced left)
        draw_superellipse_loop(
            pen,
            sx,
            sy,
            b.x1,
            ymid,
            b.x2,
            b.y2,
            hx,
            hy,
            cut="left",
        )

        # Connecting bars
        draw_rect(pen, b.x1, b.y2 - sy, b.x2 - b.width / 2, b.y2)
        draw_rect(
            pen,
            b.x1,
            ymid,
            b.x2 - b.width / 2,
            ymid + sy,
        )
