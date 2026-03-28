import pathops
from fontTools.pens.recordingPen import RecordingPen

from config import FontConfig
from shapes.rounded_loop import rounded_loop


def draw_c(pen, font_config: FontConfig, stroke: int):
    """Draw a 'c' by subtracting a rectangle from the right side of an 'o'.

    Uses pathops boolean difference for a clean subtraction — no winding
    artifacts.
    """
    rec = RecordingPen()

    # Control point offsets — clamped to half the shape dimensions
    outer_left = FontConfig.WIDTH / 2 - FontConfig.X_WIDTH / 2 - stroke / 2
    outer_right = FontConfig.WIDTH / 2 + FontConfig.X_WIDTH / 2 + stroke / 2

    rounded_loop(
        rec,
        x1=outer_left,
        y1=0,
        x2=outer_right,
        y2=FontConfig.X_HEIGHT,
        x_offset=FontConfig.X_OFFSET,
        y_offset=FontConfig.Y_OFFSET,
        stroke=stroke,
    )

    path = pathops.Path()
    rec.replay(path.getPen())

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
    result = pathops.op(path, cut, pathops.PathOp.DIFFERENCE, fix_winding=True)

    # Replay the clean result into the real pen
    result.draw(pen)
