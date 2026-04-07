from config import FontConfig as fc
from glyphs import Glyph
from draw.superellipse_arch import draw_superellipse_arch
from draw.corner import draw_corner
from draw.rect import draw_rect


class LowercaseAGlyph(Glyph):
    name = "lowercase_a"
    unicode = "0x61"
    offset = 0
    loop_ratio = 0.6

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_bottom=True,
            overshoot_left=True,
        )
        hx, hy = b.hx, b.hy * self.loop_ratio

        # Lower half half of the bowl
        arch_params = draw_superellipse_arch(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y1,
            b.x2,
            b.y1 + b.height * self.loop_ratio,
            hx,
            hy,
            taper=dc.taper_a,
            side="right",
            cut="top",
        )
        # Upper half of the bowl (corner + bar)
        draw_corner(
            pen,
            dc.stroke_x,
            dc.stroke_alt,
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
            b.y1 + b.height * self.loop_ratio - dc.stroke_alt,
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

        # Fill the gap
        (_, y1), (_, y2) = arch_params["outer"].intersection_x(x=b.x2 - dc.stroke_x)
        y1, y2 = min(y1, y2), max(y1, y2)

        draw_rect(
            pen,
            b.x2 - dc.stroke_x,
            y1,
            b.x2,
            b.y1 + b.height / 2,
        )
