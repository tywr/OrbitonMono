from glyphs import ContextualLigatureGlyph
from draw.rect import draw_rect
from draw.dented_rect import draw_dented_rect


class DoubleLowLineGlyph(ContextualLigatureGlyph):
    """Ligature glyph for __ (two consecutive underscores).

    Only fires when the run is exactly two underscores — longer runs keep
    discrete glyphs thanks to the forbidden-neighbor guard.
    """

    name = "double_low_line"
    components = ["low_line", "low_line"]
    forbidden_neighbors = ["low_line"]
    number_characters = 2
    width_ratio = 1
    stroke_ratio = 0.8

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="x_height", width_ratio=self.width_ratio
        )
        # Draw a bar that spans two full glyph widths edge-to-edge
        s = self.stroke_ratio * dc.stroke_x
        draw_dented_rect(pen, b.x1, -s, dc.window_width, 0, side="right")
        draw_dented_rect(
            pen,
            dc.window_width,
            -s,
            b.x2 + dc.window_width,
            0,
            side="left",
        )
