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


def rounded_rect(pen, left, bottom, right, top, corner_h, corner_v, clockwise=False):
    """Draw a rounded rectangle where each corner is an identical curve.

    The shape is 4 straight sides connected by 4 identical quadratic bezier
    corners. Each corner curve starts `corner_h` units from the corner along
    the horizontal edge and ends `corner_v` units from the corner along the
    vertical edge. The control point sits at the sharp corner itself.

    Args:
        left, bottom, right, top: bounding box edges.
        corner_h: horizontal extent of each corner curve — how far from
                  the corner (along x) the curve begins/ends on the
                  horizontal edges. Larger = rounder horizontal transition.
        corner_v: vertical extent of each corner curve — how far from
                  the corner (along y) the curve begins/ends on the
                  vertical edges. Larger = rounder vertical transition.
        clockwise: winding direction (True for inner counter / hole).
    """
    ch, cv = corner_h, corner_v

    if not clockwise:
        # Counter-clockwise (outer contour)
        pen.moveTo((left + ch, bottom))
        pen.lineTo((right - ch, bottom))  # bottom edge
        pen.qCurveTo((right, bottom), (right, bottom + cv))  # BR corner
        pen.lineTo((right, top - cv))  # right edge
        pen.qCurveTo((right, top), (right - ch, top))  # TR corner
        pen.lineTo((left + ch, top))  # top edge
        pen.qCurveTo((left, top), (left, top - cv))  # TL corner
        pen.lineTo((left, bottom + cv))  # left edge
        pen.qCurveTo((left, bottom), (left + ch, bottom))  # BL corner
    else:
        # Clockwise (inner contour / hole)
        pen.moveTo((left + ch, bottom))
        pen.qCurveTo((left, bottom), (left, bottom + cv))  # BL corner
        pen.lineTo((left, top - cv))  # left edge
        pen.qCurveTo((left, top), (left + ch, top))  # TL corner
        pen.lineTo((right - ch, top))  # top edge
        pen.qCurveTo((right, top), (right, top - cv))  # TR corner
        pen.lineTo((right, bottom + cv))  # right edge
        pen.qCurveTo((right, bottom), (right - ch, bottom))  # BR corner
        pen.lineTo((left + ch, bottom))  # bottom edge
    pen.closePath()
