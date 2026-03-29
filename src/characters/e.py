import pathops
from fontTools.pens.recordingPen import RecordingPen
from shapes.rounded_half_loop import rounded_half_loop
from shapes.rounded_half_loop_vertical import rounded_half_loop_vertical
from shapes.rect import rect

from config import FontConfig


def draw_e(pen, font_config: FontConfig, stroke: int):
    """Draw an 'e' from the 'o' shape: add a horizontal crossbar, then cut the bottom-right quarter."""
    # Record the full 'o' shape
    outer_left = FontConfig.WIDTH / 2 - FontConfig.X_WIDTH / 2 - stroke / 2
    outer_right = FontConfig.WIDTH / 2 + FontConfig.X_WIDTH / 2 + stroke / 2

    rounded_half_loop(
        pen,
        x1=outer_left,
        y1=0,
        x2=outer_right,
        y2=FontConfig.X_HEIGHT,
        x_offset=FontConfig.X_OFFSET,
        y_offset=FontConfig.Y_OFFSET,
        stroke=stroke,
        half="top",
    )
    rounded_half_loop_vertical(
        pen,
        x1=outer_left,
        y1=0,
        x2=outer_right,
        y2=FontConfig.X_HEIGHT,
        x_offset=FontConfig.X_OFFSET,
        y_offset=FontConfig.Y_OFFSET,
        stroke=stroke,
        half="left",
    )
    rect(
        pen,
        outer_left + stroke / 2,
        FontConfig.X_HEIGHT / 2 - stroke / 2,
        outer_right,
        FontConfig.X_HEIGHT / 2,
    )
    rect(
        pen,
        outer_left + stroke / 2,
        FontConfig.X_HEIGHT / 2,
        outer_right - stroke / 2,
        FontConfig.X_HEIGHT / 2 + stroke / 2,
    )
    rect(
        pen,
        FontConfig.WIDTH / 2,
        0,
        FontConfig.WIDTH / 2 + (FontConfig.X_WIDTH * FontConfig.E_TAIL_RATIO) / 2,
        stroke,
    )
