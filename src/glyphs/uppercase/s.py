from glyphs.uppercase import UppercaseGlyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.corner import draw_corner


class UppercaseSGlyph(UppercaseGlyph):
    name = "uppercase_s"
    unicode = "0x53"
    offset = 0
    loop_ratio = 0.5

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            height="cap",
            width_ratio=self.width_ratio,
            uppercase=True,
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio
        hx, hy = b.hx, b.hy * self.loop_ratio

        # Height of each half-loop from its respective baseline
        lh = b.height * self.loop_ratio
        ym1 = b.y1 + lh + sy / 2
        ym2 = b.y2 - lh - sy / 2

        # Bottom half-loop (cut at top)
        draw_superellipse_loop(
            pen, sx, sy, b.x1, b.y1, b.x2, ym1, hx, hy, cut="top"
        )
        # Top half-loop (cut at bottom)
        draw_superellipse_loop(
            pen, sx, sy, b.x1, ym2, b.x2, b.y2, hx, hy, cut="bottom"
        )

        # Middle left
        draw_corner(
            pen,
            sx,
            sy,
            b.x1,
            ym2 + (b.y2 - ym2) / 2,
            b.xmid,
            ym2,
            hx,
            hy,
        )

        # Middle right
        draw_corner(
            pen,
            sx,
            sy,
            b.x2,
            b.y1 + (ym1 - b.y1) / 2,
            b.xmid,
            ym1,
            hx,
            hy,
            orientation="top-left",
        )
