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
    x_corner_ratio = 0.24
    y_corner_offset = 0.075
    width_ratio = 1.2
    stroke_x_ratio = 1
    stroke_y_ratio = 1.2
    hy_ratio = 0.8

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="x_height", width_ratio=self.width_ratio
        )
        sx, sy = dc.stroke_x * self.stroke_x_ratio, dc.stroke_x * self.stroke_x_ratio
        hy = b.hy * self.hy_ratio
        h = self.height_ratio * b.height
        y1 = dc.math - h / 2 - sy / 2
        y2 = dc.math + h / 2 + sy / 2
        xi1 = b.x1 + self.x_corner_ratio * b.width + sx / 2
        xi2 = b.x2 - self.x_corner_ratio * b.width - sx / 2
        yi1 = y1 + h * self.y_corner_offset
        yi2 = y2 - h * self.y_corner_offset
        ihx = (xi2 - xi1) / 2 - sy / 4
        ehx = (xi2 - xi1) / 2 + sy / 4
        ihy = b.hy * (y2 - y1) * (1 - self.y_corner_offset) / b.height

        pen.moveTo((b.x1, yi1))
        pen.curveTo((b.x1, yi1 + hy), (xi1 - ehx, y2), (xi1, y2))
        pen.curveTo((xi1 + ehx, y2), (xi2 - ihx, y1 + sy), (xi2, y1 + sy))
        pen.curveTo((xi2 + ihx, y1 + sy), (b.x2 - sx, y2 - ihy), (b.x2 - sx, yi2))
        pen.lineTo((b.x2, yi2))
        pen.curveTo((b.x2, yi2 - hy), (xi2 + ehx, y1), (xi2, y1))
        pen.curveTo((xi2 - ehx, y1), (xi1 + ihx, y2 - sy), (xi1, y2 - sy))
        pen.curveTo((xi1 - ihx, y2 - sy), (b.x1 + sx, yi1 + ihy), (b.x1 + sx, yi1))
