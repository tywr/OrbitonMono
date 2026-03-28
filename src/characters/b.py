import pathops
from fontTools.pens.recordingPen import RecordingPen

from config import FontConfig
from characters.o import draw_o


def draw_b(pen, font_config: FontConfig, stroke: int):
    """Draw a 'b' by adding a vertical bar on the left side of an 'o'."""
    rec_o = RecordingPen()
    draw_o(rec_o, font_config=font_config, stroke=stroke, taper="left", taper_ratio=FontConfig.TAPER_RATIO)

    o_path = pathops.Path()
    rec_o.replay(o_path.getPen())

    # Left vertical bar extending to ascender height
    outer_left = FontConfig.WIDTH / 2 - FontConfig.X_WIDTH / 2 - stroke / 2
    bar_left = outer_left
    bar_right = outer_left + stroke
    bar_bottom = 0
    bar_top = FontConfig.ASCENT

    bar = pathops.Path()
    bar_pen = bar.getPen()
    bar_pen.moveTo((bar_left, bar_bottom))
    bar_pen.lineTo((bar_left, bar_top))
    bar_pen.lineTo((bar_right, bar_top))
    bar_pen.lineTo((bar_right, bar_bottom))
    bar_pen.closePath()

    result = pathops.op(o_path, bar, pathops.PathOp.UNION, fix_winding=True)
    result.draw(pen)
