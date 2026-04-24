from math import cos, sin, atan, radians
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Identity
from glyphs import Glyph
from draw.corner import draw_corner
from draw.parallelogramm import draw_parallelogramm_vertical
from utils.pens import NullPen
from draw.rect import draw_rect
from draw.parallelogramm import draw_parallelogramm_vertical


class TildeGlyph(Glyph):
    name = "tilde"
    unicode = "0x7E"
    offset = 0
    height_ratio = 0.25
    corner_ratio = 0.12
    width_ratio = 1.1
    stroke_ratio = 1.5
    hx_ratio = 0.5
    hy_ratio = 0.5

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="x_height", width_ratio=self.width_ratio
        )
        s = dc.stroke_x * self.stroke_ratio
        y1 = dc.math - self.height_ratio * b.height / 2 - s / 2
        y2 = dc.math + self.height_ratio * b.height / 2 + s / 2
        xi1 = b.x1 + self.corner_ratio * b.width + s / 2
        xi2 = b.x2 - self.corner_ratio * b.width - s / 2

        draw_parallelogramm_vertical(
            pen, s, s, b.x1, y1, xi1, y2, direction="top-right", delta=s
        )
        draw_rect(
            pen,
            xi1,
            y2 - s,
            xi1 + dc.gap,
            y2,
        )
        draw_parallelogramm_vertical(
            pen,
            s,
            s,
            xi1 + dc.gap,
            y2,
            xi2 - dc.gap,
            y1,
            delta=s,
            direction="bottom-right",
        )
        draw_rect(
            pen,
            xi2 - dc.gap,
            y1,
            xi2,
            y1 + s,
        )
        draw_parallelogramm_vertical(
            pen, s, s, xi2, y1, b.x2, y2, direction="top-right", delta=s
        )
