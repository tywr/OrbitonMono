from glyphs.uppercase import UppercaseGlyph
from draw.superellipse_loop import draw_superellipse_loop
from draw.corner import draw_corner


class UppercaseSGlyph(UppercaseGlyph):
    name = "uppercase_s"
    unicode = "0x53"
    offset = 0
    lower_loop_ratio = 0.52
    upper_loop_width = 0.96
    stroke_x_ratio = UppercaseGlyph.stroke_x_ratio * 1.05
    stroke_y_ratio = UppercaseGlyph.stroke_y_ratio * 0.95
    hx_ratio = 0.95
    hy_ratio = 1
    extra_overshoot = 0.006
    width_ratio = 1.12

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
        lhx, lhy = b.hx * self.hx_ratio, b.hy * self.lower_loop_ratio * self.hy_ratio
        uhx, uhy = (
            b.hx * self.hx_ratio * self.upper_loop_width,
            b.hy * (1 - self.lower_loop_ratio) * self.hy_ratio,
        )
        ymid = b.y1 + self.lower_loop_ratio * b.height
        ov = self.extra_overshoot * b.height

        # Height of each half-loop from its respective baseline
        lh = b.height * self.lower_loop_ratio
        uh = b.height - lh
        uw = b.width * self.upper_loop_width
        ux1, ux2 = b.xmid - uw / 2, b.xmid + uw / 2

        # Bottom half-loop (cut at top)
        draw_superellipse_loop(
            pen, sx, sy, b.x1, b.y1 - ov, b.x2, b.y1 + lh + sy / 2, lhx, lhy, cut="top"
        )
        # Top half-loop (cut at bottom)
        draw_superellipse_loop(
            pen, sx, sy, ux1, b.y2 - uh - sy / 2, ux2, b.y2 + ov, uhx, uhy, cut="bottom"
        )

        # Middle left
        draw_corner(
            pen,
            sx,
            sy,
            ux1,
            (b.y2 + ov + ymid - sy / 2) / 2,
            b.xmid,
            ymid - sy / 2,
            uhx,
            uhy,
        )

        # Middle right
        draw_corner(
            pen,
            sx,
            sy,
            b.x2,
            (ymid + sy / 2 + b.y1 - ov) / 2,
            b.xmid,
            ymid + sy / 2,
            lhx,
            lhy,
            orientation="top-left",
        )
