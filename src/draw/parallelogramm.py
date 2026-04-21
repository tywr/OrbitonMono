from math import sqrt, atan2, sin, cos
from draw.polygon import draw_polygon


def _solve_parallelogram_stroke(
    stroke_x, stroke_y, x1, y1, x2, y2, tol=1e-6, max_iter=100
):
    w = max(x2, x1) - min(x2, x1)
    h = max(y2, y1) - min(y2, y1)

    # Initial guess: angle of the bare diagonal (delta=0)
    theta = atan2(h, w)

    for _ in range(max_iter):
        s = sqrt((stroke_x * sin(theta)) ** 2 + (stroke_y * cos(theta)) ** 2)

        denom = h**2 - s**2
        if abs(denom) < 1e-12:
            break  # degenerate case

        inner = w**2 + h**2 - s**2
        if inner < 0:
            break  # stroke too thick for this geometry

        delta = (s * (h * sqrt(inner) - s * w)) / denom
        new_theta = atan2(h, w - delta)

        if abs(new_theta - theta) < tol:
            theta = new_theta
            break

        theta = new_theta

    s = sqrt((stroke_x * sin(theta)) ** 2 + (stroke_y * cos(theta)) ** 2)
    denom = h**2 - s**2
    delta = (s * (h * sqrt(w**2 + h**2 - s**2) - s * w)) / denom

    return s, delta, theta


def draw_parallelogramm(
    pen,
    stroke_x,
    stroke_y,
    x1,
    y1,
    x2,
    y2,
    direction="top-right",
    no_draw=False,
    delta=None,
):
    if delta is None:
        # w = max(x2, x1) - min(x2, x1)
        # h = max(y2, y1) - min(y2, y1)
        s, delta, theta = _solve_parallelogram_stroke(
            stroke_x, stroke_y, x1, y1, x2, y2
        )
        # s = sqrt((stroke_x * cos(theta)) ** 2 + (stroke_y * sin(theta)) ** 2)
        # delta = (s * (h * sqrt(w**2 + h**2 - s**2) - s * w)) / (h**2 - s**2)
        # theta = atan2(h, w - delta)
    else:
        # Forced delta — derive theta from the slanted-edge geometry:
        # the slanted edge has horizontal run w and vertical run h - delta,
        # so theta (angle from vertical) = atan2(w, h - delta).
        w = max(x2, x1) - min(x2, x1)
        h = max(y2, y1) - min(y2, y1)
        theta = atan2(w, h - delta)
    if no_draw:
        return theta, delta
    if direction == "top-right":
        draw_polygon(
            pen, points=[(x1, y1), (x1 + delta, y1), (x2, y2), (x2 - delta, y2)]
        )
        return theta, delta
    elif direction == "bottom-right":
        draw_polygon(
            pen, points=[(x2 - delta, y2), (x2, y2), (x1 + delta, y1), (x1, y1)]
        )
        return theta, delta
    if direction == "top-left":
        draw_polygon(
            pen, points=[(x1, y1), (x2 + delta, y2), (x2, y2), (x1 - delta, y1)]
        )
        return theta, delta
    elif direction == "bottom-left":
        draw_polygon(
            pen, points=[(x1, y1), (x1 - delta, y1), (x2, y2), (x2 + delta, y2)]
        )
        return theta, delta
    else:
        raise ValueError("Value should be either `top` or `bottom`")


def _solve_parallelogram_stroke_vertical(
    stroke_x, stroke_y, x1, y1, x2, y2, tol=1e-6, max_iter=100
):
    w = max(x2, x1) - min(x2, x1)
    h = max(y2, y1) - min(y2, y1)

    # Initial guess: angle of the bare diagonal
    theta = atan2(w, h)

    for _ in range(max_iter):
        s = sqrt((stroke_y * sin(theta)) ** 2 + (stroke_x * cos(theta)) ** 2)

        denom = w**2 - s**2
        if abs(denom) < 1e-12:
            break
        inner = w**2 + h**2 - s**2
        if inner < 0:
            break

        delta = (s * (w * sqrt(inner) - s * h)) / denom
        new_theta = atan2(w, h - delta)

        if abs(new_theta - theta) < tol:
            theta = new_theta
            break

        theta = new_theta

    s = sqrt((stroke_y * sin(theta)) ** 2 + (stroke_x * cos(theta)) ** 2)
    denom = w**2 - s**2
    delta = (s * (w * sqrt(w**2 + h**2 - s**2) - s * h)) / denom

    return s, delta, theta


def draw_parallelogramm_vertical(
    pen,
    stroke_x,
    stroke_y,
    x1,
    y1,
    x2,
    y2,
    direction="top-right",
    no_draw=False,
    delta=None,
):
    """Parallelogram with vertical parallel sides and slanted top/bottom."""
    if delta is None:
        s, delta, theta = _solve_parallelogram_stroke_vertical(
            stroke_x, stroke_y, x1, y1, x2, y2
        )
    else:
        # Forced delta — derive theta from the slanted-edge geometry:
        # the slanted edge has horizontal run w and vertical run h - delta,
        # so theta (angle from vertical) = atan2(w, h - delta).
        w = max(x2, x1) - min(x2, x1)
        h = max(y2, y1) - min(y2, y1)
        theta = atan2(w, h - delta)
    if no_draw:
        return theta, delta
    if direction == "top-right":
        draw_polygon(
            pen, points=[(x1, y1), (x2, y2 - delta), (x2, y2), (x1, y1 + delta)]
        )
        return theta, delta
    elif direction == "bottom-right":
        draw_polygon(
            pen,
            points=[
                (x1, y1),
                (x1, y1 - delta),
                (x2, y2),
                (x2, y2 + delta),
            ],
        )
        return theta, delta
    elif direction == "top-left":
        draw_polygon(
            pen,
            points=[
                (x1, y1),
                (x1, y1 + delta),
                (x2, y2),
                (x2, y2 - delta),
            ],
        )
        return theta, delta
    elif direction == "bottom-left":
        draw_polygon(
            pen, points=[(x1, y1), (x2, y2 + delta), (x2, y2), (x1, y1 - delta)]
        )
        return theta, delta
    else:
        raise ValueError("Value should be either `top` or `bottom`")


def draw_smooth_parallelogramm_vertical(
    pen,
    delta,
    x1,
    y1,
    x2,
    y2,
    radius=20,
    direction="top-right",
):
    """Parallelogram with"""
    w = max(x2, x1) - min(x2, x1)
    h = max(y2, y1) - min(y2, y1)
    theta = atan2(w, h - delta)

    if direction == "top-right":
        pen.moveTo((x1, y1))
        pen.curveTo((x1, y1), (x1 + radius, y1), (x2, y2 - delta))
        pen.lineTo((x2, y2))
        pen.curveTo((x2, y2), (x1 + radius, y1 + delta), (x1, y1 + delta))
        pen.closePath()
        return theta, delta

    elif direction == "bottom-right":
        pen.moveTo((x1, y1))
        pen.lineTo((x1, y1 - delta))
        pen.curveTo((x1 + radius, y1 - delta), (x2, y2), (x2, y2))
        pen.lineTo((x2, y2 + delta))
        pen.curveTo((x2, y2 + delta), (x1 + radius, y1), (x1, y1))
        pen.closePath()
        return theta, delta

    elif direction == "top-left":
        pen.moveTo((x1, y1))
        pen.lineTo((x1, y1 + delta))
        pen.curveTo((x1, y1 + delta), (x1 - radius, y1 + delta), (x2, y2))
        pen.lineTo((x2, y2 - delta))
        pen.curveTo((x2, y2 - delta), (x1 - radius, y1), (x1, y1))
        pen.closePath()
        return theta, delta

    elif direction == "bottom-left":
        pen.moveTo((x1, y1))
        pen.curveTo((x1, y1), (x1 - radius, y1), (x2, y2 + delta))
        pen.lineTo((x2, y2))
        pen.curveTo((x2, y2), (x1 - radius, y1 - delta), (x1, y1 - delta))
        pen.closePath()
        return theta, delta
    else:
        raise ValueError("Value should be either `top` or `bottom`")
