from glyphs import Glyph
from draw.rect import draw_rect
from draw.loop import draw_loop
from draw.polygon import draw_polygon


class QuestionMarkGlyph(Glyph):
    name = "question_mark"
    unicode = "0x3F"
    offset = 0
    width_ratio = 1
    loop_ratio = 0.6
    hx_ratio = 1
    gap = 0.35
    height_overflow = 0.05
    taper_length = 0.25
    taper = 0.75

    def draw(self, pen, dc):
        from glyphs.special.full_stop import FullStopGlyph

        b = dc.body_bounds(
            offset=self.offset,
            height="cap",
            width_ratio=self.width_ratio,
            overshoot_top=True,
            overshoot_left=True,
            overshoot_right=True,
        )
        g = self.gap * b.height
        dh = self.height_overflow * b.height
        h = self.loop_ratio * b.height
        sx, sy = dc.stroke_x, dc.stroke_y
        hx = self.hx_ratio * b.hx
        draw_loop(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y2 - h + dh,
            b.x2,
            b.y2 + dh,
            hx,
            b.hy * self.loop_ratio,
            cut="bottom",
        )
        draw_loop(
            pen,
            dc.stroke_x,
            dc.stroke_y,
            b.x1,
            b.y2 - h + dh,
            b.x2,
            b.y2 + dh,
            hx,
            b.hy * self.loop_ratio,
            cut="left",
        )
        draw_rect(
            pen,
            b.xmid - dc.stroke_x / 2,
            b.y1 + g + h * self.taper_length,
            b.xmid + dc.stroke_x / 2,
            b.y2 - h + dh + sy,
        )
        draw_polygon(
            pen,
            points=[
                (b.xmid + sx / 2, b.y1 + g + h * self.taper_length),
                (b.xmid - sx / 2, b.y1 + g + h * self.taper_length),
                (b.xmid - self.taper * sx / 2, b.y1 + g),
                (b.xmid + self.taper * sx / 2, b.y1 + g),
            ],
        )

        fsp = FullStopGlyph()
        fsp.draw(pen, dc)
