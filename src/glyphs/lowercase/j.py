from glyphs import Glyph
from draw.corner import draw_corner
from draw.rect import draw_rect


class LowercaseJGlyph(Glyph):
    name = "lowercase_j"
    unicode = "0x6A"
    offset = -50
    dot_width = 36
    tail_offset = 0
    width_ratio = 0.75
    updown_ratio = 0.9

    def draw_base(self, pen, dc):
        """Draw the letter without the dot (for use with accents)."""
        b = dc.body_bounds(offset=self.offset, width_ratio=self.width_ratio)
        # Stem
        draw_rect(pen, b.x2 - dc.stroke_x, 0, b.x2, dc.x_height)
        # Left cap
        draw_rect(
            pen,
            b.x1 + (1 - self.updown_ratio) * b.width,
            dc.x_height - dc.stroke_y,
            b.x2,
            dc.x_height,
        )
        # Corner curving down-left into the descender
        draw_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x2,
            0,
            b.xmid,
            dc.descent + self.tail_offset,
            dc.hx * 0.5,
            dc.hy,
            orientation="bottom-left",
        )
        # Extension after the corner to the left
        draw_rect(
            pen,
            b.x1,
            dc.descent + self.tail_offset,
            b.xmid,
            dc.descent + self.tail_offset + dc.stroke_y,
        )

    def draw(self, pen, dc):
        self.draw_base(pen, dc)
        b = dc.body_bounds(offset=self.offset, width_ratio=self.width_ratio)
        # Accent dot
        draw_rect(
            pen,
            b.x2 - dc.stroke_x - self.dot_width,
            dc.accent - self.dot_width / 2 - dc.stroke_x / 2,
            b.x2,
            dc.accent + dc.stroke_x / 2 + self.dot_width / 2,
        )
