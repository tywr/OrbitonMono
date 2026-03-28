import math


def _solve_quadratic(a, b, c):
    """Solve ax² + bx + c = 0, return real roots in [0, 1]."""
    if abs(a) < 1e-12:
        # Linear: bx + c = 0
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


def _eval_quad(p0, p1, p2, t):
    """Evaluate a quadratic bezier at parameter t."""
    return (1 - t) ** 2 * p0 + 2 * t * (1 - t) * p1 + t ** 2 * p2


def rounded_rect_intersect_y(x1, y1, x2, y2, radius_h, radius_v, y):
    """Find x coordinates where the rounded rect outline crosses a horizontal line y=k.

    Returns a list of (x, y) points sorted by x.
    """
    left, bottom, right, top = x1, y1, x2, y2
    ch, cv = radius_h, radius_v
    points = []

    # Left edge: x=left, from y=bottom+cv to y=top-cv
    if bottom + cv <= y <= top - cv:
        points.append((left, y))

    # Right edge: x=right, from y=bottom+cv to y=top-cv
    if bottom + cv <= y <= top - cv:
        points.append((right, y))

    # Bottom edge: y=bottom, from x=left+ch to x=right-ch (only if y == bottom)
    # Top edge: y=top, from x=left+ch to x=right-ch (only if y == top)
    if abs(y - bottom) < 1e-9:
        points.append((left + ch, y))
        points.append((right - ch, y))
    if abs(y - top) < 1e-9:
        points.append((left + ch, y))
        points.append((right - ch, y))

    # BL corner: P0=(left+ch, bottom), P1=(left, bottom), P2=(left, bottom+cv)
    for t in _solve_quadratic(
        bottom - 2 * bottom + (bottom + cv),
        2 * (bottom - bottom),
        bottom - y,
    ):
        # Recalculate properly
        pass

    # Solve each corner's quadratic bezier against y=k
    corners = [
        # (P0, P1, P2) for each corner
        # BL: bottom-left
        ((left + ch, bottom), (left, bottom), (left, bottom + cv)),
        # BR: bottom-right
        ((right - ch, bottom), (right, bottom), (right, bottom + cv)),
        # TR: top-right
        ((right, top - cv), (right, top), (right - ch, top)),
        # TL: top-left
        ((left, top - cv), (left, top), (left + ch, top)),
    ]

    # Clear previous corner attempts
    points_from_corners = []
    for p0, p1, p2 in corners:
        # Solve (1-t)²·p0y + 2t(1-t)·p1y + t²·p2y = y
        a = p0[1] - 2 * p1[1] + p2[1]
        b = 2 * (p1[1] - p0[1])
        c = p0[1] - y
        for t in _solve_quadratic(a, b, c):
            x = _eval_quad(p0[0], p1[0], p2[0], t)
            points_from_corners.append((x, y))

    points.extend(points_from_corners)

    # Deduplicate close points
    unique = []
    for p in sorted(points):
        if not unique or abs(p[0] - unique[-1][0]) > 1e-6 or abs(p[1] - unique[-1][1]) > 1e-6:
            unique.append(p)

    return unique


def rounded_rect_intersect_x(x1, y1, x2, y2, radius_h, radius_v, x):
    """Find y coordinates where the rounded rect outline crosses a vertical line x=k.

    Returns a list of (x, y) points sorted by y.
    """
    left, bottom, right, top = x1, y1, x2, y2
    ch, cv = radius_h, radius_v
    points = []

    # Bottom edge: y=bottom, from x=left+ch to x=right-ch
    if left + ch <= x <= right - ch:
        points.append((x, bottom))

    # Top edge: y=top, from x=left+ch to x=right-ch
    if left + ch <= x <= right - ch:
        points.append((x, top))

    # Left edge: x=left (only if x == left)
    if abs(x - left) < 1e-9:
        points.append((x, bottom + cv))
        points.append((x, top - cv))

    # Right edge: x=right (only if x == right)
    if abs(x - right) < 1e-9:
        points.append((x, bottom + cv))
        points.append((x, top - cv))

    # Solve each corner's quadratic bezier against x=k
    corners = [
        ((left + ch, bottom), (left, bottom), (left, bottom + cv)),
        ((right - ch, bottom), (right, bottom), (right, bottom + cv)),
        ((right, top - cv), (right, top), (right - ch, top)),
        ((left, top - cv), (left, top), (left + ch, top)),
    ]

    for p0, p1, p2 in corners:
        a = p0[0] - 2 * p1[0] + p2[0]
        b = 2 * (p1[0] - p0[0])
        c = p0[0] - x
        for t in _solve_quadratic(a, b, c):
            y = _eval_quad(p0[1], p1[1], p2[1], t)
            points.append((x, y))

    # Deduplicate close points
    unique = []
    for p in sorted(points, key=lambda p: p[1]):
        if not unique or abs(p[0] - unique[-1][0]) > 1e-6 or abs(p[1] - unique[-1][1]) > 1e-6:
            unique.append(p)

    return unique
