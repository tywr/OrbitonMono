import math

import pathops

from config import FontConfig
from characters.v import _thick_bar


def draw_k(pen, font_config: FontConfig, stroke: int):
    """Draw a lowercase 'k' — left stem from baseline to ascender, two diagonal arms."""
    outer_left = FontConfig.WIDTH / 2 - FontConfig.X_WIDTH / 2 - stroke / 2
    outer_right = FontConfig.WIDTH / 2 + FontConfig.X_WIDTH / 2 + stroke / 2
    mid_y = FontConfig.X_HEIGHT / 2

    # Left vertical stem
    stem = pathops.Path()
    sp = stem.getPen()
    sp.moveTo((outer_left, 0))
    sp.lineTo((outer_left, FontConfig.ASCENT))
    sp.lineTo((outer_left + stroke, FontConfig.ASCENT))
    sp.lineTo((outer_left + stroke, 0))
    sp.closePath()

    # Upper arm: from mid-left to top-right
    upper = _thick_bar(outer_left + stroke, mid_y, outer_right, FontConfig.X_HEIGHT, stroke)

    # Lower arm: from mid-left to bottom-right
    lower = _thick_bar(outer_left + stroke, mid_y, outer_right, 0, stroke)

    result = pathops.op(stem, upper, pathops.PathOp.UNION, fix_winding=True)
    result = pathops.op(result, lower, pathops.PathOp.UNION, fix_winding=True)

    # Clip flush at y=0 and y=ascent
    clip = pathops.Path()
    cp = clip.getPen()
    cp.moveTo((-50, 0))
    cp.lineTo((-50, FontConfig.ASCENT + 50))
    cp.lineTo((FontConfig.WIDTH + 50, FontConfig.ASCENT + 50))
    cp.lineTo((FontConfig.WIDTH + 50, 0))
    cp.closePath()

    result = pathops.op(result, clip, pathops.PathOp.INTERSECTION, fix_winding=True)

    result.draw(pen)
