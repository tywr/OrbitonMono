from glyphs import LigatureGlyph
from draw.rect import draw_rect


class DoubleHyphenMinusGlyph(LigatureGlyph):
    """Ligature glyph for -- (two consecutive hyphens).
    """

    name = "double_hyphen_minus"
    components = ["hyphen_minus", "hyphen_minus"]
    number_characters = 2
    width_ratio = 1

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="x_height", width_ratio=self.width_ratio
        )
        draw_rect(pen, b.x1, dc.math + dc.stroke_y / 2, b.x2 + dc.window_width, dc.math - dc.stroke_y / 2)
