from glyphs import Glyph
from draw.parallelogramm import draw_parallelogramm


class LowercaseWGlyph(Glyph):
    name = "lowercase_w"
    unicode = "0x77"
    offset = 0
    outer_branch_ratio = 0.25
    inner_height = 1
    width_ratio = 1.26
    stroke_ratio = 0.88
    inner_stroke_ratio = 0.74

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset,
            width_ratio=self.width_ratio,
            # min_margin=dc.min_margin_lowercase,
        )
        sx = dc.stroke_x * self.stroke_ratio
        isx = dc.stroke_x * self.inner_stroke_ratio
        xi1 = b.x1 + self.outer_branch_ratio * b.width + sx / 2
        xi2 = b.x2 - self.outer_branch_ratio * b.width - sx / 2
        yi = b.y1 + self.inner_height * b.height

        draw_parallelogramm(
            pen, 0, 0, b.x1, b.y2, xi1, b.y1, delta=sx, direction="bottom-right"
        )
        draw_parallelogramm(
            pen, 0, 0, b.x2, b.y2, xi2, b.y1, delta=sx, direction="bottom-left"
        )
        draw_parallelogramm(
            pen,
            0,
            0,
            xi1 - isx,
            b.y1,
            b.xmid + isx / 2,
            yi,
            delta=isx,
            direction="top-right",
        )
        draw_parallelogramm(
            pen,
            0,
            0,
            xi2 + isx,
            b.y1,
            b.xmid - isx / 2,
            yi,
            delta=isx,
            direction="top-left",
        )
