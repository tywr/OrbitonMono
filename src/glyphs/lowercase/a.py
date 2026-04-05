from config import FontConfig as fc
from glyph import Glyph
from shapes.superellipse_arch import draw_superellipse_arch
from shapes.corner import draw_corner
from shapes.rect import draw_rect


class LowercaseAGlyph(Glyph):
    name = "lowercase_a"
    unicode = "0x61"
    offset = 0
    loop_ratio = 0.6
    rx = 0.8

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_left=True,
        )
        # Add dampening on hx to keep ratio with the dent
        hx, hy = dc.hx * self.rx, dc.hy * self.loop_ratio

        # Lower half half of the bowl
        draw_superellipse_arch(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1,
            b.x2,
            b.y1 + b.height * self.loop_ratio,
            hx,
            hy,
            dent=dc.dent + dc.v_overshoot,
            side="right",
            cut="top",
        )
        # Upper half of the bowl (corner + bar)
        draw_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1 + b.height * self.loop_ratio / 2,
            b.xmid,
            b.y1 + b.height * self.loop_ratio,
            hx,
            hy,
            orientation="top-right",
        )
        # Middle line
        draw_rect(
            pen,
            b.xmid,
            b.y1 + b.height * self.loop_ratio - dc.stroke_y,
            b.x2 - dc.stroke_x,
            b.y1 + b.height * self.loop_ratio,
        )
        # Curve to the cap
        draw_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x2,
            b.y1 + b.height / 2,
            b.xmid,
            b.y2,
            dc.hy,
            dc.hy,
            orientation="top-left",
        )
        # Cap
        draw_rect(
            pen,
            b.x1 + dc.stroke_x / 2,
            fc.x_height - dc.stroke_y,
            b.xmid,
            fc.x_height,
        )

        # Stem
        draw_rect(
            pen,
            b.x2 - dc.stroke_x + dc.gap,
            0,
            b.x2,
            b.y1 + b.height / 2,
        )
        draw_rect(
            pen,
            b.x2 - dc.stroke_x,
            dc.dent,
            b.x2,
            b.y1 + b.height / 2,
        )
