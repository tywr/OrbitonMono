import pathops
from fontTools.pens.recordingPen import RecordingPen

from config import FontConfig
from characters.o import draw_o
from shapes import flat_hook


def draw_g(pen, font_config: FontConfig, stroke: int):
    """Draw a 'g' by adding a descender tail (flat hook) to a tapered 'o'."""
    # Record the tapered 'o' (taper on right, same as y)
    rec_o = RecordingPen()
    draw_o(rec_o, font_config=font_config, stroke=stroke, taper="right", taper_ratio=FontConfig.TAPER_RATIO)

    o_path = pathops.Path()
    rec_o.replay(o_path.getPen())

    # Same flat hook as y: right bar descending, curving left
    outer_right = FontConfig.WIDTH / 2 + FontConfig.X_WIDTH / 2 + stroke / 2
    outer_left = FontConfig.WIDTH / 2 - FontConfig.X_WIDTH / 2 - stroke / 2

    hook = pathops.Path()
    hook_pen = hook.getPen()
    flat_hook(
        hook_pen,
        corner_x=outer_right,
        corner_y=FontConfig.DESCENT + FontConfig.LOWER_HOOK_OFFSET,
        vertical_end=FontConfig.X_HEIGHT,
        horizontal_end=outer_left,
        radius=FontConfig.HOOK_RADIUS,
        stroke=stroke,
    )

    result = pathops.op(o_path, hook, pathops.PathOp.UNION, fix_winding=True)
    result.draw(pen)
