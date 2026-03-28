import math

import pathops

from config import FontConfig
from characters.v import _thick_bar


def draw_z(pen, font_config: FontConfig, stroke: int):
    """Draw a lowercase 'z' — top bar, diagonal, bottom bar."""
    outer_left = FontConfig.WIDTH / 2 - FontConfig.X_WIDTH / 2 - stroke / 2
    outer_right = FontConfig.WIDTH / 2 + FontConfig.X_WIDTH / 2 + stroke / 2
    top = FontConfig.X_HEIGHT
    bottom = 0

    # Top horizontal bar
    top_bar = pathops.Path()
    tp = top_bar.getPen()
    tp.moveTo((outer_left, top - stroke))
    tp.lineTo((outer_left, top))
    tp.lineTo((outer_right, top))
    tp.lineTo((outer_right, top - stroke))
    tp.closePath()

    # Diagonal bar from top-right to bottom-left
    diag = _thick_bar(outer_right, top, outer_left, bottom, stroke)

    # Bottom horizontal bar
    bot_bar = pathops.Path()
    bp = bot_bar.getPen()
    bp.moveTo((outer_left, bottom))
    bp.lineTo((outer_left, bottom + stroke))
    bp.lineTo((outer_right, bottom + stroke))
    bp.lineTo((outer_right, bottom))
    bp.closePath()

    result = pathops.op(top_bar, diag, pathops.PathOp.UNION, fix_winding=True)
    result = pathops.op(result, bot_bar, pathops.PathOp.UNION, fix_winding=True)

    # Clip flush at y=0 and y=x-height
    clip = pathops.Path()
    cp = clip.getPen()
    cp.moveTo((-50, bottom))
    cp.lineTo((-50, top))
    cp.lineTo((FontConfig.WIDTH + 50, top))
    cp.lineTo((FontConfig.WIDTH + 50, bottom))
    cp.closePath()

    result = pathops.op(result, clip, pathops.PathOp.INTERSECTION, fix_winding=True)

    result.draw(pen)
