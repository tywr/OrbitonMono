import pathops
from fontTools.pens.recordingPen import RecordingPen

from config import FontConfig
from characters.o import draw_o


def draw_u(pen, font_config: FontConfig, stroke: int):
    """Draw a 'u' by cutting the top half of an 'o' and adding two vertical bars.

    Left bar: short, from the cut point to x-height.
    Right bar: full height from baseline to x-height.
    """
    # Record the full 'o' shape
    rec_o = RecordingPen()
    draw_o(rec_o, font_config=font_config, stroke=stroke, taper="right", taper_ratio=FontConfig.TAPER_RATIO)

    o_path = pathops.Path()
    rec_o.replay(o_path.getPen())

    # Cut the top half — a wide rectangle from midpoint to well above x-height
    cut_y = FontConfig.X_HEIGHT / 2
    cut = pathops.Path()
    cut_pen = cut.getPen()
    cut_pen.moveTo((-50, cut_y))
    cut_pen.lineTo((-50, FontConfig.X_HEIGHT + 50))
    cut_pen.lineTo((FontConfig.WIDTH + 50, FontConfig.X_HEIGHT + 50))
    cut_pen.lineTo((FontConfig.WIDTH + 50, cut_y))
    cut_pen.closePath()

    trough = pathops.op(o_path, cut, pathops.PathOp.DIFFERENCE, fix_winding=True)

    # Left vertical bar: cut point to x-height (short left leg)
    outer_left = FontConfig.WIDTH / 2 - FontConfig.X_WIDTH / 2 - stroke / 2
    left_bar = pathops.Path()
    lp = left_bar.getPen()
    lp.moveTo((outer_left, cut_y))
    lp.lineTo((outer_left, FontConfig.X_HEIGHT))
    lp.lineTo((outer_left + stroke, FontConfig.X_HEIGHT))
    lp.lineTo((outer_left + stroke, cut_y))
    lp.closePath()

    result = pathops.op(trough, left_bar, pathops.PathOp.UNION, fix_winding=True)

    # Right vertical bar: baseline to x-height (full right stem)
    outer_right = FontConfig.WIDTH / 2 + FontConfig.X_WIDTH / 2 + stroke / 2
    right_bar = pathops.Path()
    rp = right_bar.getPen()
    rp.moveTo((outer_right - stroke, 0))
    rp.lineTo((outer_right - stroke, FontConfig.X_HEIGHT))
    rp.lineTo((outer_right, FontConfig.X_HEIGHT))
    rp.lineTo((outer_right, 0))
    rp.closePath()

    result = pathops.op(result, right_bar, pathops.PathOp.UNION, fix_winding=True)

    result.draw(pen)
