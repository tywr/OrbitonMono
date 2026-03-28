import pathops
from fontTools.pens.recordingPen import RecordingPen

from config import FontConfig
from characters.n import draw_n


def draw_h(pen, font_config: FontConfig, stroke: int):
    """Draw an 'h' by drawing an 'n' and extending the left bar to ascender height."""
    # Record the full 'n' shape
    rec_n = RecordingPen()
    draw_n(rec_n, font_config=font_config, stroke=stroke)

    n_path = pathops.Path()
    rec_n.replay(n_path.getPen())

    # Extend left bar from x-height to ascender
    outer_left = FontConfig.WIDTH / 2 - FontConfig.X_WIDTH / 2 - stroke / 2
    ext = pathops.Path()
    ep = ext.getPen()
    ep.moveTo((outer_left, 0))
    ep.lineTo((outer_left, FontConfig.ASCENT))
    ep.lineTo((outer_left + stroke, FontConfig.ASCENT))
    ep.lineTo((outer_left + stroke, 0))
    ep.closePath()

    result = pathops.op(n_path, ext, pathops.PathOp.UNION, fix_winding=True)
    result.draw(pen)
