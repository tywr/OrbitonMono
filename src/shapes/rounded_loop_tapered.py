from shapes.rounded_rect import rounded_rect, rounded_rect_asym


def rounded_loop_tapered(
    pen,
    x1,
    y1,
    x2,
    y2,
    x_offset,
    y_offset,
    x_offset_taper,
    y_offset_taper,
    stroke,
    ratio_taper,
    direction="right",
):
    """Draw a loop with asymmetric curve offsets on one side.

    One side uses (x_offset, y_offset), the tapered side uses
    (x_offset_taper, y_offset_taper). This allows the loop to have
    a different curvature on the tapered side (e.g. where it meets a stem).

    Args:
        x1, y1: bottom-left corner of the outer bounding box.
        x2, y2: top-right corner of the outer bounding box.
        x_offset: horizontal control point offset for the normal side.
        y_offset: vertical control point offset for the normal side.
        x_offset_taper: horizontal control point offset for the tapered side.
        y_offset_taper: vertical control point offset for the tapered side.
        stroke: thickness of the loop walls.
        direction: "left" or "right" — which side gets the tapered offsets.
    """
    # Taper shrinks the outer edge on the tapered side
    taper_inset = (1 - ratio_taper) * stroke
    if direction == "right":
        xo_left, yo_left = x_offset, y_offset
        xo_right, yo_right = x_offset_taper, y_offset_taper
        outer_x2 = x2 - taper_inset
        outer_x1 = x1
    else:
        xo_left, yo_left = x_offset_taper, y_offset_taper
        xo_right, yo_right = x_offset, y_offset
        outer_x1 = x1 + taper_inset
        outer_x2 = x2

    # Outer contour (CCW)
    rounded_rect_asym(
        pen,
        outer_x1,
        y1,
        outer_x2,
        y2,
        x_offset_left=xo_left,
        y_offset_left=yo_left,
        x_offset_right=xo_right,
        y_offset_right=yo_right,
        clockwise=False,
    )

    # Inner contour (CW) — uses original x1/x2 inset by full stroke,
    # so the tapered side has a thinner wall (ratio_taper * stroke).
    inner_x1 = x1 + stroke
    inner_x2 = x2 - stroke
    inner_y1 = y1 + stroke
    inner_y2 = y2 - stroke

    outer_half_w = (x2 - x1) / 2
    outer_half_h = (y2 - y1) / 2
    inner_half_w = (inner_x2 - inner_x1) / 2
    inner_half_h = (inner_y2 - inner_y1) / 2

    ratio_w = inner_half_w / outer_half_w if outer_half_w > 0 else 0
    ratio_h = inner_half_h / outer_half_h if outer_half_h > 0 else 0

    inner_xo = x_offset * ratio_w
    inner_yo = y_offset * ratio_h

    rounded_rect(
        pen,
        x1=inner_x1,
        y1=inner_y1,
        x2=inner_x2,
        y2=inner_y2,
        x_offset=inner_xo,
        y_offset=inner_yo,
        clockwise=True,
    )

    return {
        "x1": outer_x1,
        "y1": y1,
        "x2": outer_x2,
        "y2": y2,
        "x_offset_left": xo_left,
        "y_offset_left": yo_left,
        "x_offset_right": xo_right,
        "y_offset_right": yo_right,
    }
