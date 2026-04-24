from glyphs.accents import Accent


class Tilde(Accent):
    name = "accent_tilde"
    unicode = None
    rescale = 0.7

    def draw_at(self, pen, dc, x, y):
        from glyphs.special.tilde import TildeGlyph
        from fontTools.pens.recordingPen import RecordingPen
        from fontTools.pens.transformPen import TransformPen
        from fontTools.misc.transform import Transform

        oy = dc.accent - dc.math
        r = self.rescale

        # Record the tilde glyph
        rec = RecordingPen()
        TildeGlyph().draw(rec, dc)

        # Scale around the cell center, then offset vertically by oy
        cx = dc.window_width / 2
        cy = dc.math
        t = Transform()
        t = t.translate(cx, cy + oy)
        t = t.scale(r)
        t = t.translate(-cx, -cy)

        rec.replay(TransformPen(pen, t))
