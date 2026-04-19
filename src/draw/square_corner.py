def draw_square_corner(
    pen,
    stroke_x,
    stroke_y,
    x1,
    y1,
    x2,
    y2,
    radius=100,
    orientation="bottom-right",
):
    """Draw a solid L-corner with the external (outer) corner rounded.

    (x1, y1) is the outer start of the stroke, (x2, y2) is the outer end.
    The outer corner sits at (x1, y2) and is rounded with `radius`; the
    inner corner stays sharp. The stroke extends inward by (stroke_x,
    stroke_y) from the outer edges.
    """
    sign_x = +1 if "right" in orientation else -1
    sign_y = +1 if "bottom" in orientation else -1

    ix1 = x1 + sign_x * stroke_x
    iy1 = y1
    ix2 = x2
    iy2 = y2 + sign_y * stroke_y

    p0 = (x1, y2 + sign_y * radius)
    p1 = (x1, y2 + sign_y * radius / 2)
    p2 = (x1 + sign_x * radius / 2, y2)
    p3 = (x1 + sign_x * radius, y2)

    pen.moveTo((x1, y1))
    pen.lineTo(p0)
    pen.curveTo(p1, p2, p3)
    pen.lineTo((x2, y2))
    pen.lineTo((ix2, iy2))
    pen.lineTo((ix1, iy2))
    pen.lineTo((ix1, iy1))
    pen.closePath()
