import pathops
from fontTools.pens.recordingPen import RecordingPen

from config import FontConfig
from characters.n import draw_n


def draw_r(pen, font_config: FontConfig, stroke: int):
    """Draw an 'r' by removing the right side of an 'n' below a threshold.

    Args:
        right_cut: fraction of x-height below which the right side is removed.
                   0.3 means everything below 30% of x-height on the right is cut.
    """
    rec_n = RecordingPen()
    draw_n(rec_n, font_config=font_config, stroke=stroke)

    n_path = pathops.Path()
    rec_n.replay(n_path.getPen())

    # Cut rectangle: right half, from below baseline to right_cut * x-height
    cut_y = FontConfig.R_CUT * FontConfig.X_HEIGHT
    mid_x = FontConfig.WIDTH / 2

    cut = pathops.Path()
    cut_pen = cut.getPen()
    cut_pen.moveTo((mid_x, -50))
    cut_pen.lineTo((mid_x, cut_y))
    cut_pen.lineTo((FontConfig.WIDTH + 50, cut_y))
    cut_pen.lineTo((FontConfig.WIDTH + 50, -50))
    cut_pen.closePath()

    result = pathops.op(n_path, cut, pathops.PathOp.DIFFERENCE, fix_winding=True)
    result.draw(pen)
