def rounded_rect(pen, x1, y1, x2, y2, radius_v, radius_h, clockwise=False):
    """Draw a rounded rectangle where each corner is an identical curve.

    The shape is 4 straight sides connected by 4 identical quadratic bezier
    corners. Each corner curve starts `radius_h` units from the corner along
    the horizontal edge and ends `radius_v` units from the corner along the
    vertical edge. The control point sits at the sharp corner itself.

    Args:
        x1, y1: bottom-left corner of the bounding box.
        x2, y2: top-right corner of the bounding box.
        radius_v: vertical extent of each corner curve.
        radius_h: horizontal extent of each corner curve.
        clockwise: winding direction (True for inner counter / hole).
    """
    left, bottom, right, top = x1, y1, x2, y2
    ch, cv = radius_h, radius_v

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
