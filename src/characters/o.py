from config import FontConfig
from shapes import rounded_rect


def draw_o(pen, font_config: FontConfig, stroke: int):
    """Draw a tall rounded-rectangle 'o' with generous corner rounding."""
    height = FontConfig.X_HEIGHT
    outer_left = FontConfig.WIDTH / 2 - FontConfig.X_WIDTH / 2 - stroke / 2
    outer_right = FontConfig.WIDTH / 2 + FontConfig.X_WIDTH / 2 + stroke / 2

    # Outer shape
    rounded_rect(
        pen,
        left=outer_left,
        bottom=0,
        right=outer_right,
        top=font_config.X_HEIGHT,
        corner_h=175,
        corner_v=200,
        clockwise=False,
    )
    # Inner counter (hole)
    rounded_rect(
        pen,
        left=outer_left + stroke,
        bottom=stroke,
        right=outer_right - stroke,
        top=height - stroke,
        corner_h=175 - stroke,
        corner_v=200 - stroke,
        clockwise=True,
    )
