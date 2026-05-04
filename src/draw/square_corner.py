def draw_square_corner(
    pen,
    stroke_x,
    stroke_y,
    x1,
    y1,
    x2,
    y2,
    gx=200,
    gy=200,
    orientation="bottom-right",
):
    """Draw a solid quarter-curve corner using superellipse handles.

    (x1, y1) is the outer start of the curve, (x2, y2) is the outer end.
    The stroke always goes inward (away from the corner).

    The corner point is at (x2, y1) or (x1, y2) depending on orientation:
        bottom-right: corner at (x2, y1) — curve goes right then up
        top-right:    corner at (x1, y2) — curve goes up then right
        top-left:     corner at (x2, y1) — curve goes left then down
        bottom-left:  corner at (x1, y2) — curve goes down then left
    """
    w = abs(x2 - x1)
    h = abs(y2 - y1)
    sx, sy = stroke_x, stroke_y

    if orientation == "bottom-left":
        pen.moveTo((x1, y1))
        pen.lineTo((x1, y2 + gy))
        pen.curveTo((x1, y2 + sy / 2), (x1 - sx / 2, y2), (x1 - gx, y2))
        pen.lineTo((x2, y2))
        pen.lineTo((x2, y2 + sy))
        pen.lineTo((x1 - sx - gx, y2 + sy))
        pen.curveTo((x1 - sx, y2 + sy), (x1 - sx, y2 + sy), (x1 - sx, y2 + sy + gy))
        pen.lineTo((x1 - sx, y1))
        pen.closePath()

    elif orientation == "bottom-right":
        pen.moveTo((x1, y1))
        pen.lineTo((x1, y2 + gy))
        pen.curveTo((x1, y2 + sy / 2), (x1 + sx / 2, y2), (x1 + gx, y2))
        pen.lineTo((x2, y2))
        pen.lineTo((x2, y2 + sy))
        pen.lineTo((x1 + sx + gx, y2 + sy))
        pen.curveTo((x1 + sx, y2 + sy), (x1 + sx, y2 + sy), (x1 + sx, y2 + sy + gy))
        pen.lineTo((x1 + sx, y1))
        pen.closePath()

    elif orientation == "top-left":
        pen.moveTo((x1, y1))
        pen.lineTo((x1, y2 - gy))
        pen.curveTo((x1, y2 - sy / 2), (x1 - sx / 2, y2), (x1 - gx, y2))
        pen.lineTo((x2, y2))
        pen.lineTo((x2, y2 - sy))
        pen.lineTo((x1 - sx - gx, y2 - sy))
        pen.curveTo((x1 - sx, y2 - sy), (x1 - sx, y2 - sy), (x1 - sx, y2 - sy - gy))
        pen.lineTo((x1 - sx, y1))
        pen.closePath()

    elif orientation == "top-right":
        pen.moveTo((x1, y1))
        pen.lineTo((x1, y2 - gy))
        pen.curveTo((x1, y2 - sy / 2), (x1 + sx / 2, y2), (x1 + gx, y2))
        pen.lineTo((x2, y2))
        pen.lineTo((x2, y2 - sy))
        pen.lineTo((x1 + sx + gx, y2 - sy))
        pen.curveTo((x1 + sx, y2 - sy), (x1 + sx, y2 - sy), (x1 + sx, y2 - sy - gy))
        pen.lineTo((x1 + sx, y1))
        pen.closePath()
