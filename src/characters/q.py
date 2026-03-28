import pathops
from fontTools.pens.recordingPen import RecordingPen

from config import FontConfig
from characters.o import draw_o


def draw_q(pen, font_config: FontConfig, stroke: int):
    """Draw a 'q' by adding a vertical bar on the right side of an 'o', extending to descender."""
    rec_o = RecordingPen()
    draw_o(rec_o, font_config=font_config, stroke=stroke, taper="right", taper_ratio=FontConfig.TAPER_RATIO)

    o_path = pathops.Path()
    rec_o.replay(o_path.getPen())

    # Right vertical bar extending to descender depth
    outer_right = FontConfig.WIDTH / 2 + FontConfig.X_WIDTH / 2 + stroke / 2
    bar_left = outer_right - stroke
    bar_right = outer_right
    bar_bottom = FontConfig.DESCENT
    bar_top = FontConfig.X_HEIGHT

    bar = pathops.Path()
    bar_pen = bar.getPen()
    bar_pen.moveTo((bar_left, bar_bottom))
    bar_pen.lineTo((bar_left, bar_top))
    bar_pen.lineTo((bar_right, bar_top))
    bar_pen.lineTo((bar_right, bar_bottom))
    bar_pen.closePath()

    result = pathops.op(o_path, bar, pathops.PathOp.UNION, fix_winding=True)
    result.draw(pen)
