import math


def _solve_cubic_roots_01(a, b, c, d):
    """Find real roots of ax³ + bx² + cx + d = 0 in [0, 1]."""
    # Normalize
    if abs(a) < 1e-12:
        # Degenerate to quadratic
        return _solve_quadratic(b, c, d)

    # Use numerical approach: sample and refine with Newton's method
    roots = []
    n = 64
    prev = a * 0 + b * 0 + c * 0 + d
    for i in range(1, n + 1):
        t = i / n
        val = a * t**3 + b * t**2 + c * t + d
        if abs(val) < 1e-12:
            roots.append(t)
        elif prev * val < 0:
            # Sign change — bisect
            lo, hi = (i - 1) / n, t
            for _ in range(50):
                mid = (lo + hi) / 2
                fmid = a * mid**3 + b * mid**2 + c * mid + d
                if abs(fmid) < 1e-12:
                    break
                if fmid * (a * lo**3 + b * lo**2 + c * lo + d) < 0:
                    hi = mid
                else:
                    lo = mid
            roots.append((lo + hi) / 2)
        prev = val

    return roots


def _solve_quadratic(a, b, c):
    """Solve ax² + bx + c = 0, return real roots in [0, 1]."""
    if abs(a) < 1e-12:
        if abs(b) < 1e-12:
            return []
        t = -c / b
        return [t] if 0 <= t <= 1 else []

    disc = b * b - 4 * a * c
    if disc < 0:
        return []

    sqrt_disc = math.sqrt(disc)
    roots = []
    for t in [(-b - sqrt_disc) / (2 * a), (-b + sqrt_disc) / (2 * a)]:
        if 0 <= t <= 1:
            roots.append(t)
    return roots


def _eval_cubic(p0, p1, p2, p3, t):
    """Evaluate a cubic bezier at parameter t."""
    u = 1 - t
    return u**3 * p0 + 3 * u**2 * t * p1 + 3 * u * t**2 * p2 + t**3 * p3


def rounded_rect_intersect_y(x1, y1, x2, y2, x_offset, y_offset, y):
    """Find x coordinates where the rounded rect outline crosses a horizontal line y=k.

    Returns a list of (x, y) points sorted by x.
    """
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    points = []

    # The shape has 4 cubic bezier curves connecting midpoints.
    # Each curve: (start, cp1, cp2, end) with x and y coordinates.
    curves = [
        # Bottom-right: bottom_mid → right_mid
        ((mid_x, y1), (mid_x + x_offset, y1), (x2, mid_y - y_offset), (x2, mid_y)),
        # Top-right: right_mid → top_mid
        ((x2, mid_y), (x2, mid_y + y_offset), (mid_x + x_offset, y2), (mid_x, y2)),
        # Top-left: top_mid → left_mid
        ((mid_x, y2), (mid_x - x_offset, y2), (x1, mid_y + y_offset), (x1, mid_y)),
        # Bottom-left: left_mid → bottom_mid
        ((x1, mid_y), (x1, mid_y - y_offset), (mid_x - x_offset, y1), (mid_x, y1)),
    ]

    for p0, p1, p2, p3 in curves:
        # Solve for t where y(t) = y
        a = -p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]
        b = 3 * p0[1] - 6 * p1[1] + 3 * p2[1]
        c = -3 * p0[1] + 3 * p1[1]
        d = p0[1] - y
        for t in _solve_cubic_roots_01(a, b, c, d):
            x_val = _eval_cubic(p0[0], p1[0], p2[0], p3[0], t)
            points.append((x_val, y))

    # Deduplicate close points
    unique = []
    for p in sorted(points):
        if not unique or abs(p[0] - unique[-1][0]) > 1e-6 or abs(p[1] - unique[-1][1]) > 1e-6:
            unique.append(p)

    return unique


def rounded_rect_intersect_x(x1, y1, x2, y2, x_offset, y_offset, x):
    """Find y coordinates where the rounded rect outline crosses a vertical line x=k.

    Returns a list of (x, y) points sorted by y.
    """
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    points = []

    curves = [
        ((mid_x, y1), (mid_x + x_offset, y1), (x2, mid_y - y_offset), (x2, mid_y)),
        ((x2, mid_y), (x2, mid_y + y_offset), (mid_x + x_offset, y2), (mid_x, y2)),
        ((mid_x, y2), (mid_x - x_offset, y2), (x1, mid_y + y_offset), (x1, mid_y)),
        ((x1, mid_y), (x1, mid_y - y_offset), (mid_x - x_offset, y1), (mid_x, y1)),
    ]

    for p0, p1, p2, p3 in curves:
        a = -p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]
        b = 3 * p0[0] - 6 * p1[0] + 3 * p2[0]
        c = -3 * p0[0] + 3 * p1[0]
        d = p0[0] - x
        for t in _solve_cubic_roots_01(a, b, c, d):
            y_val = _eval_cubic(p0[1], p1[1], p2[1], p3[1], t)
            points.append((x, y_val))

    # Deduplicate close points
    unique = []
    for p in sorted(points, key=lambda p: p[1]):
        if not unique or abs(p[0] - unique[-1][0]) > 1e-6 or abs(p[1] - unique[-1][1]) > 1e-6:
            unique.append(p)

    return unique


def rounded_rect_asym_intersect_x(
    x1, y1, x2, y2,
    x_offset_left, y_offset_left,
    x_offset_right, y_offset_right,
    x,
):
    """Find y coordinates where an asymmetric rounded rect crosses a vertical line x=k.

    Returns a list of (x, y) points sorted by y.
    """
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2

    curves = [
        # Bottom-right
        ((mid_x, y1), (mid_x + x_offset_right, y1), (x2, mid_y - y_offset_right), (x2, mid_y)),
        # Top-right
        ((x2, mid_y), (x2, mid_y + y_offset_right), (mid_x + x_offset_right, y2), (mid_x, y2)),
        # Top-left
        ((mid_x, y2), (mid_x - x_offset_left, y2), (x1, mid_y + y_offset_left), (x1, mid_y)),
        # Bottom-left
        ((x1, mid_y), (x1, mid_y - y_offset_left), (mid_x - x_offset_left, y1), (mid_x, y1)),
    ]

    points = []
    for p0, p1, p2, p3 in curves:
        a = -p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]
        b = 3 * p0[0] - 6 * p1[0] + 3 * p2[0]
        c = -3 * p0[0] + 3 * p1[0]
        d = p0[0] - x
        for t in _solve_cubic_roots_01(a, b, c, d):
            y_val = _eval_cubic(p0[1], p1[1], p2[1], p3[1], t)
            points.append((x, y_val))

    unique = []
    for p in sorted(points, key=lambda p: p[1]):
        if not unique or abs(p[0] - unique[-1][0]) > 1e-6 or abs(p[1] - unique[-1][1]) > 1e-6:
            unique.append(p)

    return unique
