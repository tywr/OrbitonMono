def flat_hook(pen, corner_x, corner_y, vertical_end, horizontal_end, radius, stroke):
    """Draw a thick L-shaped stroke with a rounded corner.

    The shape is a vertical line that curves into a horizontal line via a
    quadratic bezier with the given radius.

    Args:
        corner_x, corner_y: the outer corner point — where the vertical
                            and horizontal edges would meet if sharp.
        vertical_end: y coordinate where the vertical part ends (away from
                      the corner). Above corner_y = upward, below = downward.
        horizontal_end: x coordinate where the horizontal part ends (away
                        from the corner). Right of corner_x = rightward,
                        left = leftward.
        radius: outer corner radius.
        stroke: thickness of the stroke.
    """
    # Determine directions
    goes_up = vertical_end > corner_y
    goes_right = horizontal_end > corner_x

    # Sign multipliers for stroke offset direction
    # Stroke expands inward: for a bottom-left corner going up and right,
    # the stroke goes to the right on the vertical and upward on the horizontal.
    sx = 1 if goes_right else -1  # horizontal direction
    sy = 1 if goes_up else -1    # vertical direction

    # Inner corner radius (may be 0 if stroke >= radius)
    inner_r = max(0, radius - stroke)

    # Outer path: follows the outside of the stroke
    # Inner path: follows the inside, offset by stroke

    # Points on outer edge
    ov_end = (corner_x, vertical_end)                          # vertical end
    ov_curve_start = (corner_x, corner_y + sy * radius)        # where curve begins on vertical
    oh_curve_end = (corner_x + sx * radius, corner_y)          # where curve ends on horizontal
    oh_end = (horizontal_end, corner_y)                        # horizontal end

    # Points on inner edge (offset by stroke)
    ih_end = (horizontal_end, corner_y + sy * stroke)          # horizontal end, inner
    if inner_r > 0:
        ih_curve_start = (corner_x + sx * (radius), corner_y + sy * stroke)  # inner horizontal before curve
        # Actually, inner curve start on horizontal side
        ih_curve_start = (corner_x + sx * inner_r + sx * stroke, corner_y + sy * stroke)
        iv_curve_end = (corner_x + sx * stroke, corner_y + sy * inner_r + sy * stroke)
    else:
        # No inner radius — sharp inner corner
        ih_curve_start = (corner_x + sx * stroke, corner_y + sy * stroke)
        iv_curve_end = None
    iv_end = (corner_x + sx * stroke, vertical_end)            # vertical end, inner

    # Draw CCW contour
    pen.moveTo(ov_end)
    pen.lineTo(ov_curve_start)
    pen.qCurveTo((corner_x, corner_y), oh_curve_end)
    pen.lineTo(oh_end)
    pen.lineTo(ih_end)
    if iv_curve_end is not None:
        pen.lineTo(ih_curve_start)
        pen.qCurveTo((corner_x + sx * stroke, corner_y + sy * stroke), iv_curve_end)
    else:
        pen.lineTo(ih_curve_start)
    pen.lineTo(iv_end)
    pen.closePath()
