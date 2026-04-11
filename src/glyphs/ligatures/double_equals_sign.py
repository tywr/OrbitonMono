from glyphs import LigatureGlyph
from draw.rect import draw_rect


class DoubleEqualsSignGlyph(LigatureGlyph):
    """Ligature glyph for == (two consecutive underscores).

    Draws a single continuous bar spanning the full width of two cells
    (2 * window_width), creating a seamless connection between underscores.
    """

    name = "double_equals_sign"
    components = ["equals_sign", "equals_sign"]
    number_characters = 2
    width_ratio = 1
    gap = 0.4

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="x_height", width_ratio=self.width_ratio
        )
        g = self.gap * b.height
        draw_rect(
            pen,
            b.x1,
            dc.math + g / 2 - dc.stroke_y / 2,
            b.x2 + dc.window_width,
            dc.math + g / 2 + dc.stroke_y / 2,
        )
        draw_rect(
            pen,
            b.x1,
            dc.math - g / 2 - dc.stroke_y / 2,
            b.x2 + dc.window_width,
            dc.math - g / 2 + dc.stroke_y / 2,
        )
