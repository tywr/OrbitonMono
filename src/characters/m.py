import pathops
from fontTools.pens.recordingPen import RecordingPen

from config import FontConfig
from characters.o import draw_o


def draw_m(pen, font_config: FontConfig, stroke: int):
    """Draw an 'm' using two narrow arches side by side.

    Left arch: tapered o, bottom cut, with a full left stem.
    Right arch: non-tapered o, bottom cut, with a short right descender.
    The two arches share a middle stem via pathops union.
    """
    cut_y = FontConfig.X_HEIGHT / 2
    outer_left = FontConfig.WIDTH / 2 - FontConfig.X_WIDTH / 2 - stroke / 2
    outer_right = FontConfig.WIDTH / 2 + FontConfig.X_WIDTH / 2 + stroke / 2
    mid_x = FontConfig.WIDTH / 2

    # --- Left arch: tapered o centered on left half ---
    left_center = (outer_left + mid_x + stroke / 2) / 2
    rec_left = RecordingPen()
    draw_o(rec_left, font_config=font_config, stroke=stroke,
           taper="left", taper_ratio=FontConfig.TAPER_RATIO,
           center_x=left_center, x_ratio=0.5)

    left_path = pathops.Path()
    rec_left.replay(left_path.getPen())

    # Cut bottom half
    cut = pathops.Path()
    cp = cut.getPen()
    cp.moveTo((-50, -50))
    cp.lineTo((-50, cut_y))
    cp.lineTo((FontConfig.WIDTH + 50, cut_y))
    cp.lineTo((FontConfig.WIDTH + 50, -50))
    cp.closePath()

    left_arch = pathops.op(left_path, cut, pathops.PathOp.DIFFERENCE, fix_winding=True)

    # Left vertical bar: baseline to x-height
    left_bar = pathops.Path()
    lp = left_bar.getPen()
    lp.moveTo((outer_left, 0))
    lp.lineTo((outer_left, FontConfig.X_HEIGHT))
    lp.lineTo((outer_left + stroke, FontConfig.X_HEIGHT))
    lp.lineTo((outer_left + stroke, 0))
    lp.closePath()

    result = pathops.op(left_arch, left_bar, pathops.PathOp.UNION, fix_winding=True)

    # --- Right arch: non-tapered o centered on right half ---
    right_center = (mid_x + outer_right - stroke / 2) / 2
    rec_right = RecordingPen()
    draw_o(rec_right, font_config=font_config, stroke=stroke,
           center_x=right_center, x_ratio=0.5)

    right_path = pathops.Path()
    rec_right.replay(right_path.getPen())

    right_arch = pathops.op(right_path, cut, pathops.PathOp.DIFFERENCE, fix_winding=True)

    result = pathops.op(result, right_arch, pathops.PathOp.UNION, fix_winding=True)

    # Right vertical bar: baseline to cut point (short right leg)
    right_bar = pathops.Path()
    rp = right_bar.getPen()
    rp.moveTo((outer_right - stroke, 0))
    rp.lineTo((outer_right - stroke, cut_y))
    rp.lineTo((outer_right, cut_y))
    rp.lineTo((outer_right, 0))
    rp.closePath()

    result = pathops.op(result, right_bar, pathops.PathOp.UNION, fix_winding=True)

    result.draw(pen)
