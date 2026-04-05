def draw_corner(
    pen,
    stroke_x,
    stroke_y,
    x1, y1,
    x2, y2,
    hx, hy,
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
    ihx = hx * (w - stroke_x) / w if w > 0 else 0
    ihy = hy * (h - stroke_y) / h if h > 0 else 0

    if orientation == "bottom-left":
        # Corner at (x1, y2). Start on right, end on bottom.
        ix1 = x1 - stroke_x
        iy1 = y1
        ix2 = x2
        iy2 = y2 + stroke_y

        pen.moveTo((ix1, iy1))
        pen.curveTo((ix1, iy1 - ihy), (ix2 + ihx, iy2), (ix2, iy2))
        pen.lineTo((x2, y2))
        pen.curveTo((x2 + hx, y2), (x1, y1 - hy), (x1, y1))
        pen.closePath()

    elif orientation == "top-left":
        # Corner at (x1, y2). Start on right, end on top.
        ix1 = x1 - stroke_x
        iy1 = y1
        ix2 = x2
        iy2 = y2 - stroke_y

        pen.moveTo((x1, y1))
        pen.curveTo((x1, y1 + hy), (x2 + hx, y2), (x2, y2))
        pen.lineTo((ix2, iy2))
        pen.curveTo((ix2 + ihx, iy2), (ix1, iy1 + ihy), (ix1, iy1))
        pen.closePath()

    elif orientation == "top-right":
        # Corner at (x1, y2). Start on left, end on top.
        ix1 = x1 + stroke_x
        iy1 = y1
        ix2 = x2
        iy2 = y2 - stroke_y

        pen.moveTo((ix1, iy1))
        pen.curveTo((ix1, iy1 + ihy), (ix2 - ihx, iy2), (ix2, iy2))
        pen.lineTo((x2, y2))
        pen.curveTo((x2 - hx, y2), (x1, y1 + hy), (x1, y1))
        pen.closePath()

    elif orientation == "bottom-right":
        # Corner at (x1, y2). Start on left, end on bottom.
        ix1 = x1 + stroke_x
        iy1 = y1
        ix2 = x2
        iy2 = y2 + stroke_y

        pen.moveTo((x1, y1))
        pen.curveTo((x1, y1 - hy), (x2 - hx, y2), (x2, y2))
        pen.lineTo((ix2, iy2))
        pen.curveTo((ix2 - ihx, iy2), (ix1, iy1 - ihy), (ix1, iy1))
        pen.closePath()
