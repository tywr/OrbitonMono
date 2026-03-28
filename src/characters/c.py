import pathops
from fontTools.pens.recordingPen import RecordingPen

from config import FontConfig
from characters.o import draw_o


def draw_c(pen, font_config: FontConfig, stroke: int):
    """Draw a 'c' by subtracting a rectangle from the right side of an 'o'.

    Uses pathops boolean difference for a clean subtraction — no winding
    artifacts.
    """
    # Record the full 'o' shape
    rec = RecordingPen()
    draw_o(rec, font_config=font_config, stroke=stroke)

    o_path = pathops.Path()
    rec.replay(o_path.getPen())

    # Build the cut rectangle (extends well beyond the outer edge)
    outer_right = FontConfig.WIDTH
    inner_right = FontConfig.WIDTH / 2
    gap_y_bottom = int(FontConfig.C_GAP_BOTTOM * FontConfig.X_HEIGHT)
    gap_y_top = int(FontConfig.C_GAP_TOP * FontConfig.X_HEIGHT)

    cut = pathops.Path()
    cut_pen = cut.getPen()
    cut_pen.moveTo((inner_right, gap_y_bottom))
    cut_pen.lineTo((inner_right, gap_y_top))
    cut_pen.lineTo((outer_right + 50, gap_y_top))
    cut_pen.lineTo((outer_right + 50, gap_y_bottom))
    cut_pen.closePath()

    # Boolean difference: o minus cut
    result = pathops.op(o_path, cut, pathops.PathOp.DIFFERENCE, fix_winding=True)

    # Replay the clean result into the real pen
    result.draw(pen)
