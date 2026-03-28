import pathops
from fontTools.pens.recordingPen import RecordingPen

from config import FontConfig
from characters.o import draw_o


def draw_d(pen, font_config: FontConfig, stroke: int):
    """Draw a 'd' by adding a vertical bar on the right side of an 'o'.

    Uses pathops boolean union for a clean merge — no overlapping contours.
    """
    # Record the full 'o' shape
    rec_o = RecordingPen()
    draw_o(rec_o, font_config=font_config, stroke=stroke)

    o_path = pathops.Path()
    rec_o.replay(o_path.getPen())

    # Build the right vertical bar (ascender height)
    outer_right = FontConfig.WIDTH / 2 + FontConfig.X_WIDTH / 2 + stroke / 2
    bar_left = outer_right - stroke
    bar_right = outer_right
    bar_bottom = 0
    bar_top = FontConfig.ASCENT

    bar = pathops.Path()
    bar_pen = bar.getPen()
    bar_pen.moveTo((bar_left, bar_bottom))
    bar_pen.lineTo((bar_left, bar_top))
    bar_pen.lineTo((bar_right, bar_top))
    bar_pen.lineTo((bar_right, bar_bottom))
    bar_pen.closePath()

    # Boolean union: o + bar
    result = pathops.op(o_path, bar, pathops.PathOp.UNION, fix_winding=True)

    # Replay the clean result into the real pen
    result.draw(pen)
