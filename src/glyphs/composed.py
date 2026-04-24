from abc import ABC
from glyphs import Glyph


class ComposedGlyph(Glyph, ABC):
    """A glyph composed of a base glyph and an accent mark.

    Subclasses declare base_glyph_class, accent_class, and positioning.
    The accent is drawn centered on the base glyph's body bounds at accent_y.
    """

    base_glyph_class = None
    accent_class = None
    accent_y = None  # vertical position for the accent anchor
    accent_x_offset = 0  # horizontal adjustment if needed

    @property
    def offset(self):
        return self.base_glyph_class.offset

    def draw(self, pen, dc):
        base = self.base_glyph_class()
        base.draw_base(pen, dc) if hasattr(base, "draw_base") else base.draw(pen, dc)

        b = dc.body_bounds(offset=self.offset)
        accent_y = self.accent_y if self.accent_y is not None else dc.accent
        self.accent_class().draw_at(pen, dc, x=b.xmid + self.base_glyph_class.accent_x_offset, y=accent_y)
