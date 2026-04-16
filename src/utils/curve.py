def split_curve(p0, p1, p2, p3, t):
    """Returns the first segment of a cubic bezier split at t."""
    # Lerp level 1
    q0 = lerp(p0, p1, t)
    q1 = lerp(p1, p2, t)
    q2 = lerp(p2, p3, t)
    # Lerp level 2
    r0 = lerp(q0, q1, t)
    r1 = lerp(q1, q2, t)
    # Lerp level 3 — this is the point on the curve at t
    s0 = lerp(r0, r1, t)

    # The first half is: p0 -> q0, r0, s0
    return q0, r0, s0  # new cp1, cp2, endpoint


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
