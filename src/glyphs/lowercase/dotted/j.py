from glyphs import Glyph
from draw.square_corner import draw_square_corner
from draw.rect import draw_rect
from glyphs.lowercase.dotted import DottedLowercaseGlyph


class LowercaseJGlyph(DottedLowercaseGlyph):
    name = "lowercase_j"
    unicode = "0x6A"
    offset = 88
    tail_offset = 0
    width_ratio = 1.4
    updown_ratio = 1

    def draw_base(self, pen, dc):
        """Draw the letter without the dot (for use with accents)."""
        b = dc.body_bounds(offset=self.offset, width_ratio=self.width_ratio)
        x2 = b.xmid + dc.stroke_x / 2
        # Stem
        draw_rect(pen, x2 - dc.stroke_x, 0, x2, dc.x_height)
        # Left cap
        draw_rect(
            pen,
            b.x1 + (1 - self.updown_ratio) * b.width,
            dc.x_height - dc.stroke_y,
            x2,
            dc.x_height,
        )
        # Corner curving down-left into the descender
        draw_square_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            x2,
            0,
            b.xmid,
            dc.descent + self.tail_offset,
            # dc.hx * 0.5,
            # dc.hy,
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
