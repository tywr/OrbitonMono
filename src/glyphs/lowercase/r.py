from glyphs import Glyph
from draw.arch import draw_arch
from draw.rect import draw_rect
from draw.polygon import draw_polygon


class LowercaseRGlyph(Glyph):
    name = "lowercase_r"
    unicode = "0x72"
    offset = 10
    loop_ratio = 0.92
    hx_ratio = 1.05
    hy_ratio = 1
    taper = 0.5
    ending_thickness = 0.8
    width_ratio = 1
    tail_offset = 0.03

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            overshoot_top=True,
            width_ratio=self.width_ratio,
        )
        hx, hy = dc.hx * self.hx_ratio, dc.hy * self.hy_ratio
        ys = b.y2 - self.loop_ratio * b.height
        xt = b.x2 - self.tail_offset * b.width

        arch_params = draw_arch(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            ys,
            xt,
            b.y2,
            hx,
            hy,
            taper=self.taper * dc.taper,
            side="left",
            cut="bottom",
        )

        # Left stem
        draw_rect(pen, b.x1, 0, b.x1 + dc.stroke_x, dc.x_height)
