"""Smooth corner with Euler-spiral (clothoid) curvature distribution.

Approximates a quarter-turn curve with two cubic Bézier segments whose
curvature tapers to zero at the junctions with straight segments — the
hallmark of an Euler spiral transition.

The unit Euler spiral for a symmetric quarter turn is precomputed at
import time via numerical Fresnel integration, then affine-transformed
to match each corner's geometry at draw time.
"""

import math


# ── Precompute unit Euler spiral quarter turn ─────────────────────────────
#
# The symmetric clothoid quarter turn has curvature that rises linearly
# from 0 to κ_max at the midpoint, then falls linearly back to 0.
#
# Parametrised by arc length t ∈ [0, 2]:
#   First half  (t ∈ [0, 1]):  θ(t) = π t² / 4        (0° → 45°)
#   Second half (t ∈ [1, 2]):  θ(t) = πt − πt²/4 − π/2 (45° → 90°)
#
# By symmetry, the endpoint satisfies Ex = Ey = Mx + My.


def _integrate_half(s_max, n=10000):
    """Numerically integrate the first half of the Euler spiral."""
    dt = s_max / n
    x = y = 0.0
    for i in range(1, n + 1):
        t = i * dt
        theta = math.pi * t * t / 4.0
        x += math.cos(theta) * dt
        y += math.sin(theta) * dt
    return x, y


_MX, _MY = _integrate_half(1.0)       # midpoint (tangent at 45°)
_E = _MX + _MY                        # Ex = Ey (tangent at 90°)

# Determine handle parameter α by matching the Bézier at t = 0.5
# to the actual spiral at arc-length s = 0.5.
#
# First-half Bézier: P0=(0,0) P1=(α,0) P2=(Mx−My,0) P3=(Mx,My)
# Bx(½) = 3α/8 + 3(Mx−My)/8 + Mx/8  =  3α/8 + Mx/2 − 3My/8
_TARGET_X, _ = _integrate_half(0.5)
_ALPHA = (_TARGET_X - 0.5 * _MX + 0.375 * _MY) * 8.0 / 3.0

# Unit control points — two cubic Bézier segments
# Segment 1 (0° → 45°):  zero curvature at start (P0, P1, P2 collinear)
# Segment 2 (45° → 90°): zero curvature at end   (Q1, Q2, Q3 collinear)
_U1 = ((0.0, 0.0), (_ALPHA, 0.0), (_MX - _MY, 0.0), (_MX, _MY))
_U2 = ((_MX, _MY), (_E, 2.0 * _MY), (_E, _E - _ALPHA), (_E, _E))


# ── Helpers ───────────────────────────────────────────────────────────────

def _lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def _split_half(p0, p1, p2, p3):
    """De Casteljau split at t = 0.5."""
    q0 = _lerp(p0, p1, 0.5)
    q1 = _lerp(p1, p2, 0.5)
    q2 = _lerp(p2, p3, 0.5)
    r0 = _lerp(q0, q1, 0.5)
    r1 = _lerp(q1, q2, 0.5)
    s = _lerp(r0, r1, 0.5)
    return (p0, q0, r0, s), (s, r1, q2, p3)


def _euler_segments(p0, p1, p2, p3):
    """Two Euler-spiral cubic segments matching the original cubic's
    endpoints and tangent directions."""
    d0 = (p1[0] - p0[0], p1[1] - p0[1])
    d3 = (p3[0] - p2[0], p3[1] - p2[1])
    chord = (p3[0] - p0[0], p3[1] - p0[1])

    len0 = math.hypot(*d0)
    len3 = math.hypot(*d3)
    if len0 < 1e-10 or len3 < 1e-10:
        return _split_half(p0, p1, p2, p3)

    n0 = (d0[0] / len0, d0[1] / len0)
    n3 = (d3[0] / len3, d3[1] / len3)
    cross = n0[0] * n3[1] - n0[1] * n3[0]
    if abs(cross) < 1e-10:
        return _split_half(p0, p1, p2, p3)

    # Solve for scale factors a, b so that
    #   a·n0·Ex + b·n3·Ey = chord   (with Ex = Ey = _E)
    a = (chord[0] * n3[1] - chord[1] * n3[0]) / (_E * cross)
    b = (chord[1] * n0[0] - chord[0] * n0[1]) / (_E * cross)

    def xform(v):
        return (
            p0[0] + a * n0[0] * v[0] + b * n3[0] * v[1],
            p0[1] + a * n0[1] * v[0] + b * n3[1] * v[1],
        )

    return (
        tuple(xform(u) for u in _U1),
        tuple(xform(u) for u in _U2),
    )


def _smooth_bezier(p0, p1, p2, p3, smooth):
    """Blend between the original cubic (smooth=0) and the Euler-spiral
    two-segment approximation (smooth=1)."""
    if smooth <= 0:
        return [(p0, p1, p2, p3)]

    s = min(smooth, 1.0)
    dc1, dc2 = _split_half(p0, p1, p2, p3)
    eu1, eu2 = _euler_segments(p0, p1, p2, p3)

    seg1 = tuple(_lerp(dc1[i], eu1[i], s) for i in range(4))
    seg2 = tuple(_lerp(dc2[i], eu2[i], s) for i in range(4))
    return [seg1, seg2]


# ── Public API ────────────────────────────────────────────────────────────

def draw_smooth_corner(
    pen,
    stroke_x,
    stroke_y,
    x1,
    y1,
    x2,
    y2,
    hx,
    hy,
    orientation="bottom-right",
    smooth=0.6,
):
    """Draw a solid quarter-curve corner with Euler-spiral smoothing.

    Same geometry as draw_corner.  *smooth* (0–1) controls how much
    curvature tapers to zero at the junctions with straight segments.
    smooth=0 reproduces draw_corner exactly.
    """
    w = abs(x2 - x1)
    h = abs(y2 - y1)
    ihx = hx * (w - stroke_x) / w if w > 0 else 0
    ihy = hy * (h - stroke_y) / h if h > 0 else 0

    if orientation == "bottom-left":
        ix1, iy1 = x1 - stroke_x, y1
        ix2, iy2 = x2, y2 + stroke_y
        curve1 = ((ix1, iy1), (ix1, iy1 - ihy), (ix2 + ihx, iy2), (ix2, iy2))
        curve2 = ((x2, y2), (x2 + hx, y2), (x1, y1 - hy), (x1, y1))

    elif orientation == "top-left":
        ix1, iy1 = x1 - stroke_x, y1
        ix2, iy2 = x2, y2 - stroke_y
        curve1 = ((x1, y1), (x1, y1 + hy), (x2 + hx, y2), (x2, y2))
        curve2 = ((ix2, iy2), (ix2 + ihx, iy2), (ix1, iy1 + ihy), (ix1, iy1))

    elif orientation == "top-right":
        ix1, iy1 = x1 + stroke_x, y1
        ix2, iy2 = x2, y2 - stroke_y
        curve1 = ((ix1, iy1), (ix1, iy1 + ihy), (ix2 - ihx, iy2), (ix2, iy2))
        curve2 = ((x2, y2), (x2 - hx, y2), (x1, y1 + hy), (x1, y1))

    elif orientation == "bottom-right":
        ix1, iy1 = x1 + stroke_x, y1
        ix2, iy2 = x2, y2 + stroke_y
        curve1 = ((x1, y1), (x1, y1 - hy), (x2 - hx, y2), (x2, y2))
        curve2 = ((ix2, iy2), (ix2 - ihx, iy2), (ix1, iy1 - ihy), (ix1, iy1))

    segs1 = _smooth_bezier(*curve1, smooth)
    segs2 = _smooth_bezier(*curve2, smooth)

    pen.moveTo(segs1[0][0])
    for seg in segs1:
        pen.curveTo(seg[1], seg[2], seg[3])
    pen.lineTo(segs2[0][0])
    for seg in segs2:
        pen.curveTo(seg[1], seg[2], seg[3])
    pen.closePath()
