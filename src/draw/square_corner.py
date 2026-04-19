def draw_square_corner(
    pen,
    stroke_x,
    stroke_y,
    x1,
    y1,
    x2,
    y2,
    gx=25,
    gy=50,
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

    if orientation == "bottom-left":
        ix1 = x1 - stroke_x
        iy1 = y1
        ix2 = x2
        iy2 = y2 + stroke_y
        xc1, yc1 = x1, y1 - h + stroke_y + gy
        xc2, yc2 = x2 + w - stroke_x - gx, y2

        pen.moveTo((x1, y1))
        pen.lineTo((ix1, iy1))
        pen.lineTo((ix1, yc1))
        pen.curveTo((ix1, y2 + stroke_x), (ix2 + stroke_x, iy2), (ix2, iy2))
        pen.lineTo((x2, y2))
        pen.lineTo((xc2, yc2))
        pen.curveTo((xc2 + stroke_x, yc2), (xc1, yc1 - stroke_y), (xc1, yc1))
        pen.closePath()

    elif orientation == "bottom-right":
        ix1 = x1 + stroke_x
        iy1 = y1
        ix2 = x2
        iy2 = y2 + stroke_y
        xc1, yc1 = x1, y2 + stroke_y + gy
        xc2, yc2 = x1 + stroke_x + gx, y2

        pen.moveTo((x1, y1))
        pen.lineTo((xc1, yc1))
        pen.curveTo((xc1, yc1 - stroke_y), (xc2 - stroke_x, yc2), (xc2, yc2))
        pen.lineTo((x2, y2))
        pen.lineTo((ix2, iy2))
        pen.lineTo((ix1, iy2))
        pen.lineTo((ix1, iy1))
        pen.closePath()

    elif orientation == "top-left":
        ix1 = x1 - stroke_x
        iy1 = y1
        ix2 = x2
        iy2 = y2 - stroke_y
        xc1, yc1 = x1, y2 - stroke_y - gy
        xc2, yc2 = x1 - stroke_x - gx, y2

        pen.moveTo((x1, y1))
        pen.lineTo((xc1, yc1))
        pen.curveTo((xc1, yc1 + stroke_y), (xc2 + stroke_x, yc2), (xc2, yc2))
        pen.lineTo((x2, y2))
        pen.lineTo((ix2, iy2))
        pen.lineTo((ix1, iy2))
        pen.lineTo((ix1, iy1))
        pen.closePath()

    elif orientation == "top-right":
        ix1 = x1 + stroke_x
        iy1 = y1
        ix2 = x2
        iy2 = y2 - stroke_y
        xc1, yc1 = x1, y2 - stroke_y - gy
        xc2, yc2 = x1 + stroke_x + gx, y2

        pen.moveTo((x1, y1))
        pen.lineTo((ix1, iy1))
        pen.lineTo((ix1, iy2))
        pen.lineTo((ix2, iy2))
        pen.lineTo((x2, y2))
        pen.lineTo((xc2, yc2))
        pen.curveTo((xc2 - stroke_x, yc2), (xc1, yc1 + stroke_y), (xc1, yc1))
        pen.closePath()
