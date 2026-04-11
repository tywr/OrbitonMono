from glyphs import LigatureGlyph
from draw.rect import draw_rect


class DoubleLowLineGlyph(LigatureGlyph):
    """Ligature glyph for __ (two consecutive underscores).

    Draws a single continuous bar spanning the full width of two cells
    (2 * window_width), creating a seamless connection between underscores.
    """

    name = "double_low_line"
    components = ["low_line", "low_line"]
    number_characters = 2
    width_ratio = 1

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="x_height", width_ratio=self.width_ratio
        )
        # Draw a bar that spans two full glyph widths edge-to-edge
        draw_rect(pen, b.x1, -dc.stroke_y, b.x2 + dc.window_width, 0)
