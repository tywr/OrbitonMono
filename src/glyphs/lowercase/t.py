from glyphs import Glyph
from draw.corner import draw_corner
from draw.rect import draw_rect


class LowercaseTGlyph(Glyph):
    name = "lowercase_t"
    unicode = "0x74"
    offset = -40
    rl_ratio = 0.55  # Right/left split of the cross-bar and footer
    up_ratio = 0.28

    def draw(self, pen, dc):
        b = dc.body_bounds(offset=self.offset, height="x_height")
        right_len = b.width * self.rl_ratio - dc.stroke_x / 2
        left_len = b.width * (1 - self.rl_ratio) - dc.stroke_x / 2

        # Stem
        draw_rect(
            pen,
            b.xmid - dc.stroke_x / 2,
            b.ymid,
            b.xmid + dc.stroke_x / 2,
            (1 + self.up_ratio) * dc.x_height,
        )
        # Cross-bar at x_height
        draw_rect(
            pen,
            b.xmid - left_len - dc.stroke_x / 2,
            dc.x_height - dc.stroke_y,
            b.xmid + right_len + dc.stroke_x / 2,
            dc.x_height,
        )
        # Corner curving down-right (shorter/flatter than f)
        draw_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.xmid - dc.stroke_x / 2,
            b.ymid,
            b.xmid + b.width / 2,
            0,
            b.width / 2 + dc.stroke_x / 2,
            b.height / 2,
            orientation="bottom-right",
        )
        # Footer extension from corner to right edge
        draw_rect(
            pen,
            b.xmid + b.width / 2,
            0,
            b.xmid + right_len + dc.stroke_x / 2,
            dc.stroke_y,
        )
