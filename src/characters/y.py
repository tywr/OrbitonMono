import pathops
from fontTools.pens.recordingPen import RecordingPen

from config import FontConfig
from characters.u import draw_u
from shapes import flat_hook


def draw_y(pen, font_config: FontConfig, stroke: int):
    """Draw a 'y' by adding a descender tail (flat hook) to a 'u'."""
    # Record the full 'u' shape
    rec_u = RecordingPen()
    draw_u(rec_u, font_config=font_config, stroke=stroke)

    u_path = pathops.Path()
    rec_u.replay(u_path.getPen())

    # Add a flat hook on the right bar, descending and curving left
    outer_right = FontConfig.WIDTH / 2 + FontConfig.X_WIDTH / 2 + stroke / 2
    outer_left = FontConfig.WIDTH / 2 - FontConfig.X_WIDTH / 2 - stroke / 2

    hook = pathops.Path()
    hook_pen = hook.getPen()
    flat_hook(
        hook_pen,
        corner_x=outer_right,          # outer right edge of the right bar
        corner_y=FontConfig.DESCENT + FontConfig.LOWER_HOOK_OFFSET,   # bottom of the descender
        vertical_end=stroke,           # up to baseline area (overlaps with u)
        horizontal_end=outer_left,     # hook extends left
        radius=FontConfig.HOOK_RADIUS,
        stroke=stroke,
    )

    result = pathops.op(u_path, hook, pathops.PathOp.UNION, fix_winding=True)
    result.draw(pen)
