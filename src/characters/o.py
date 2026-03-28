from config import FontConfig
from shapes import rounded_rect


def draw_o(pen, font_config: FontConfig, stroke: int,
           taper=None, taper_ratio=1.0):
    """Draw a tall rounded-rectangle 'o' with generous corner rounding.

    Args:
        taper: "left" or "right" — which side gets a thinner stroke.
               None means uniform stroke on both sides.
        taper_ratio: 0.0 to 1.0 — fraction of stroke on the tapered side.
                     1.0 = full stroke (no taper), 0.0 = zero stroke.
    """
    height = FontConfig.X_HEIGHT
    inner_left = FontConfig.WIDTH / 2 - FontConfig.X_WIDTH / 2 + stroke / 2
    inner_right = FontConfig.WIDTH / 2 + FontConfig.X_WIDTH / 2 - stroke / 2

    # Outer edges — full stroke by default, reduced on tapered side
    left_stroke = stroke * taper_ratio if taper == "left" else stroke
    right_stroke = stroke * taper_ratio if taper == "right" else stroke

    outer_left = inner_left - left_stroke
    outer_right = inner_right + right_stroke

    # Corner params scale with the stroke on each side
    base_corner_h = 175
    base_corner_v = 200
    outer_corner_h = base_corner_h
    outer_corner_v = base_corner_v

    # Clamp so corners don't exceed half the shape width
    max_ch = (outer_right - outer_left) / 2
    outer_corner_h = min(outer_corner_h, max_ch)

    # Outer shape
    rounded_rect(
        pen,
        left=outer_left,
        bottom=0,
        right=outer_right,
        top=font_config.X_HEIGHT,
        corner_h=outer_corner_h,
        corner_v=outer_corner_v,
        clockwise=False,
    )
    # Inner counter (hole) — always unchanged
    rounded_rect(
        pen,
        left=inner_left,
        bottom=stroke,
        right=inner_right,
        top=height - stroke,
        corner_h=base_corner_h - stroke,
        corner_v=base_corner_v - stroke,
        clockwise=True,
    )
