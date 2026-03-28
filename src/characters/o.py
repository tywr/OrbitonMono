from config import FontConfig
from shapes import rounded_rect


def draw_o(
    pen,
    font_config: FontConfig,
    stroke: int,
    taper=None,
    taper_ratio=1.0,
    center_x=None,
    x_ratio=1.0,
):
    """Draw a tall rounded-rectangle 'o' with generous corner rounding.

    Args:
        taper: "left" or "right" — which side gets a thinner stroke.
               None means uniform stroke on both sides.
        taper_ratio: 0.0 to 1.0 — fraction of stroke on the tapered side.
                     1.0 = full stroke (no taper), 0.0 = zero stroke.
        center_x: horizontal center of the glyph. Defaults to FontConfig.WIDTH / 2.
        x_ratio: horizontal compression factor. 1.0 = normal, <1.0 = narrower.
                 Scales the counter width and horizontal corner radius,
                 but keeps stroke unchanged.
    """
    if center_x is None:
        center_x = FontConfig.WIDTH / 2
    height = FontConfig.X_HEIGHT
    half_width = FontConfig.X_WIDTH / 2 * x_ratio
    inner_left = center_x - half_width + stroke / 2
    inner_right = center_x + half_width - stroke / 2

    # Outer edges — full stroke by default, reduced on tapered side
    left_stroke = stroke * taper_ratio if taper == "left" else stroke
    right_stroke = stroke * taper_ratio if taper == "right" else stroke

    outer_left = inner_left - left_stroke
    outer_right = inner_right + right_stroke

    # Corner params — stay at full size, clamped to fit the shape.
    # Narrow shapes (x_ratio < 1) get fully rounded tops with no flat parts.
    h_radius = FontConfig.H_RADIUS
    v_radius = FontConfig.V_RADIUS

    # Clamp so corners don't exceed half the shape dimensions
    max_ch = (outer_right - outer_left) / 2
    max_cv = font_config.X_HEIGHT / 2
    outer_corner_h = min(h_radius, max_ch)
    v_radius = min(v_radius, max_cv)

    # Outer shape
    rounded_rect(
        pen,
        left=outer_left,
        bottom=0,
        right=outer_right,
        top=font_config.X_HEIGHT,
        corner_h=outer_corner_h,
        corner_v=v_radius,
        clockwise=False,
    )

    # Inner corner params — computed from the inner contour's own dimensions
    inner_width = inner_right - inner_left
    inner_height = (height - stroke) - stroke
    inner_corner_h = min(h_radius, inner_width / 2)
    inner_corner_v = min(v_radius, inner_height / 2)

    # Inner shape
    rounded_rect(
        pen,
        left=inner_left,
        bottom=stroke,
        right=inner_right,
        top=height - stroke,
        corner_h=inner_corner_h,
        corner_v=inner_corner_v,
        clockwise=True,
    )
