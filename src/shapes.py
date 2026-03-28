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
