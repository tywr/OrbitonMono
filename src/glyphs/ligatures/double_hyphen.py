from glyphs import ContextualLigatureGlyph
from draw.dented_rect import draw_dented_rect


class DoubleHyphenGlyph(ContextualLigatureGlyph):
    """Ligature glyph for -- (two consecutive hyphens).

    Only fires when the run is exactly two hyphens — longer runs keep
    discrete glyphs thanks to the forbidden-neighbor guard.
    """

    name = "double_hyphen"
    components = ["hyphen_minus", "hyphen_minus"]
    forbidden_neighbors = ["hyphen_minus"]
    number_characters = 2
    width_ratio = 0.88
    stroke_ratio = 0.8

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="x_height", width_ratio=self.width_ratio
        )
        s = dc.stroke_x * self.stroke_ratio
        o = (1 - self.width_ratio) * b.width / 2
        # Draw a bar that spans two full glyph widths edge-to-edge
        draw_dented_rect(
            pen, b.x1 + o, dc.math - s / 2, dc.window_width, dc.math + s / 2, side="right"
        )
        draw_dented_rect(
            pen,
            dc.window_width,
            dc.math - s / 2,
            b.x2 + dc.window_width - o,
            dc.math + s / 2,
            side="left",
        )
