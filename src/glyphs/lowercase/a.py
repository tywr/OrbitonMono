from glyphs import Glyph
from draw.superellipse_arch import draw_superellipse_arch
from draw.corner import draw_corner
from draw.rect import draw_rect
from draw.parallelogramm import draw_parallelogramm_vertical
from draw.polygon import draw_polygon


class LowercaseAGlyph(Glyph):
    name = "lowercase_a"
    unicode = "0x61"
    offset = -11
    loop_ratio = 0.6
    width_ratio = 1
    stroke_x_ratio = 1.04
    stroke_y_ratio = 0.96
    taper = 0.3
    cap_ratio = 0.6
    cap_width = 0.96
    cap_radius = 1.618
    cap_right_hx_ratio = 1
    cap_right_hy_ratio = 0.8
    overshoot_reducing = 0.5
    cap_offset = 0.08
    ending_thickness = 0.8

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_top=True,
            overshoot_bottom=True,
            overshoot_left=True,
            width_ratio=self.width_ratio,
        )
        sx, sy = self.stroke_x_ratio * dc.stroke_x, self.stroke_y_ratio * dc.stroke_y
        dx = sx - dc.stroke_x
        hx, hy = b.hx, b.hy * self.loop_ratio
        yc = b.y1 + self.cap_ratio * b.height
        crhx, crhy = self.cap_right_hx_ratio * b.hx, self.cap_right_hy_ratio * b.hy
        yt = dc.x_height - dc.stroke_y - dc.v_overshoot
        xt = b.x1 + self.cap_offset * b.width

        # Lower half half of the bowl
        arch_params = draw_superellipse_arch(
            pen,
            sx,
            sy,
            b.x1,
            b.y1,
            b.x2 + dx,
            b.y1 + b.height * self.loop_ratio,
            hx,
            hy,
            taper=self.taper,
            side="right",
            cut="top",
        )
        # Upper half of the bowl (corner + bar)
        draw_corner(
            pen,
            sx,
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


        # Cap
        draw_corner(
            pen,
            sx,
            dc.stroke_y,
            b.x2,
            yc,
            b.xmid,
            # b.y2 - self.overshoot_reducing * dc.v_overshoot,
            b.y2,
            crhx,
            crhy,
            orientation="top-left",
        )
        theta, delta = draw_parallelogramm_vertical(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.xmid,
            b.y2,
            xt,
            yt,
            direction="bottom-left",
            delta=dc.stroke_y,
        )

        # Fill the gap
        (_, y1), (_, y2) = arch_params["outer"].intersection_x(
            x=b.x2 - dc.stroke_x - dc.gap
        )
        y1, y2 = min(y1, y2), max(y1, y2)

        # Stem
        draw_rect(
            pen,
            b.x2 - sx,
            y1,
            b.x2,
            yc,
        )

        draw_polygon(
            pen,
            points=[
                (b.x2 - self.ending_thickness * dc.stroke_x, 0),
                (b.x2, 0),
                (b.x2, y1),
                (b.x2 - dc.stroke_x, y1),
            ],
        )

        # Fill the gap
        draw_polygon(
            pen,
            points=[
                (b.x2 - dc.stroke_x - dc.gap, y1),
                (b.x2 - dc.stroke_x, y1),
                (b.x2 - dc.stroke_x + dc.stroke_x * dc.taper / 2, b.ymid),
            ],
        )
