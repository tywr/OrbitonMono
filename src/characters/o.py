from config import FontConfig
from shapes.rounded_rect import rounded_rect
from shapes.rect import rect
from shapes.intersect import rounded_rect_intersect_x


def draw_o(
    pen,
    font_config: FontConfig,
    stroke: int,
    taper=None,
    taper_ratio=1.0,
    center_x=None,
    x_ratio=1.0,
    height=None,
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
    if height is None:
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
    max_cv = height / 2
    outer_corner_h = min(h_radius, max_ch)
    outer_corner_v = min(v_radius, max_cv)

    # Outer shape
    rounded_rect(
        pen,
        x1=outer_left,
        y1=0,
        x2=outer_right,
        y2=height,
        radius_v=outer_corner_v,
        radius_h=outer_corner_h,
        clockwise=False,
    )

    # Inner corners — derived from the non-tapered outer dimensions
    # so the inner shape stays identical regardless of taper
    full_outer_width = (inner_right + stroke) - (inner_left - stroke)
    full_corner_h = min(h_radius, full_outer_width / 2)
    inner_corner_h = max(0, full_corner_h - stroke)
    inner_corner_v = max(0, outer_corner_v - stroke)

    # Inner shape
    rounded_rect(
        pen,
        x1=inner_left,
        y1=stroke,
        x2=inner_right,
        y2=height - stroke,
        radius_v=inner_corner_v,
        radius_h=inner_corner_h,
        clockwise=True,
    )

    # Ink trap squares at tapered side junctions
    # The square sticks out from the curve at the intersection point,
    # extending away from the loop (toward the stem side).
    ink = FontConfig.INK_TRAP
    if taper == "left" and ink > 0:
        full_left = inner_left - stroke
        hits = rounded_rect_intersect_x(
            outer_left, 0, outer_right, height,
            outer_corner_h, outer_corner_v, inner_left,
        )
        if len(hits) >= 2:
            _, y_bottom = hits[0]
            _, y_top = hits[-1]
            # Bottom: square below and left of the curve
            rect(pen, inner_left, y_bottom - ink, inner_left + stroke / 2, y_bottom)
            # Top: square above and left of the curve
            rect(pen, inner_left, y_top, inner_left + stroke /2 , y_top + ink)

    elif taper == "right" and ink > 0:
        full_right = inner_right + stroke
        hits = rounded_rect_intersect_x(
            outer_left, 0, outer_right, height,
            outer_corner_h, outer_corner_v, inner_right,
        )
        if len(hits) >= 2:
            _, y_bottom = hits[0]
            _, y_top = hits[-1]
            # Bottom: square below and right of the curve
            rect(pen, inner_right - stroke / 2, y_bottom - ink, inner_right, y_bottom)
            # Top: square above and right of the curve
            rect(pen, inner_right - stroke / 2, y_top, inner_right, y_top + ink)
