import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph
from glyphs import Glyph
from draw.square_corner import draw_square_corner
from draw.rect import draw_rect
from draw.polygon import draw_polygon


class LowercaseTGlyph(Glyph):
    name = "lowercase_t"
    unicode = "0x74"
    offset = -45
    width_ratio = 1.1
    rl_ratio = 0.55
    up_ratio = 0.28

    def draw(self, pen, dc):
        b = dc.body_bounds(
            offset=self.offset, height="x_height", width_ratio=self.width_ratio
        )
        right_len = b.width * self.rl_ratio - dc.stroke_x / 2
        left_len = b.width * (1 - self.rl_ratio) - dc.stroke_x / 2

        # Cross-bar at x_height
        draw_rect(
            pen,
            b.xmid - left_len - dc.stroke_x / 2,
            dc.x_height - dc.stroke_y,
            b.xmid + right_len + dc.stroke_x / 2,
            dc.x_height,
        )
        # Corner curving down-right (shorter/flatter than f)
        draw_square_corner(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.xmid - dc.stroke_x / 2,
            b.ymid,
            b.xmid + b.width / 2,
            0,
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

        glyph = ufoLib2.objects.Glyph()

        # Stem
        draw_rect(
            glyph.getPen(),
            b.xmid - dc.stroke_x / 2,
            b.ymid,
            b.xmid + dc.stroke_x / 2,
            (1 + self.up_ratio) * dc.x_height,
        )
        cut_glyph = ufoLib2.objects.Glyph()

        draw_polygon(
            cut_glyph.getPen(),
            points=[
                (b.xmid + dc.stroke_x / 2, (1 + self.up_ratio) * dc.x_height),
                (
                    b.xmid - left_len - dc.stroke_x / 2,
                    dc.x_height,
                ),
                (
                    b.xmid - left_len - dc.stroke_x / 2,
                    (1 + self.up_ratio) * dc.x_height,
                ),
            ],
        )
        res = BooleanGlyph(glyph).difference(BooleanGlyph(cut_glyph))
        res.draw(pen)
