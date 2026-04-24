from glyphs.uppercase import UppercaseGlyph
from draw.rect import draw_rect
from draw.superellipse_loop import draw_superellipse_loop
from draw.corner import draw_corner
from draw.parallelogramm import draw_parallelogramm_vertical


class UppercaseJGlyph(UppercaseGlyph):
    name = "uppercase_j"
    unicode = "0x4A"
    offset = -6
    cap_ratio = 1
    hx_ratio = 1
    loop_ratio = 0.6
    tail_len = 0.5

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            overshoot_bottom=True,
            width_ratio=self.width_ratio,
        )
        hx, hy = self.hx_ratio * b.hx, dc.hy
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_y * self.stroke_y_ratio
        xc = self.cap_ratio * b.width
        xt = b.xmid - self.tail_len * b.width
        yt = sy + dc.v_overshoot

        # Vertical stem (centered)
        # draw_rect(pen, b.x2 - sx, b.y1 + self.loop_ratio * b.height / 2, b.x2, b.y2)
        draw_rect(pen, b.x2 - sx, b.ymid, b.x2, b.y2)

        # Top bar
        draw_rect(pen, b.x2 - xc, b.y2 - sy, b.x2, b.y2)

        # Corner to bottom
        draw_corner(pen, sx, sy, b.x2, b.ymid, b.xmid, b.y1, hx, hy, orientation="bottom-left")

        draw_parallelogramm_vertical(
            pen,
            sx,
            sy,
            b.xmid,
            b.y1,
            xt,
            yt,
            direction="top-left",
            delta=sy
        )
