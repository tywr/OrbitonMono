from glyphs import Glyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.cross_curve import draw_cross_curve
from draw.corner import draw_corner


class LowercaseSGlyph(Glyph):
    name = "lowercase_s"
    unicode = "0x73"
    offset = 0
    loop_ratio = 0.5  # Controls the height of each half-loop

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_top=True,
            overshoot_left=True,
            overshoot_right=True,
        )
        hx, hy = b.hx, b.hy * self.loop_ratio

        # Height of each half-loop from its respective baseline
        lh = b.height * self.loop_ratio
        ym1 = b.y1 + lh + dc.stroke_y / 2
        ym2 = b.y2 - lh - dc.stroke_y / 2

        # Bottom half-loop (cut at top)
        draw_superellipse_loop(
            pen, dc.stroke_x, dc.stroke_y, b.x1, b.y1, b.x2, ym1, hx, hy, cut="top"
        )
        # Top half-loop (cut at bottom)
        draw_superellipse_loop(
            pen, dc.stroke_x, dc.stroke_y, b.x1, ym2, b.x2, b.y2, hx, hy, cut="bottom"
        )

        # Middle left
        draw_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
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
            dc.stroke_x,
            dc.stroke_y,
            b.x2,
            b.y1 + (ym1 - b.y1) / 2,
            b.xmid,
            ym1,
            hx,
            hy,
            orientation="top-left"
        )
