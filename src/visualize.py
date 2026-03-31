#!/usr/bin/env python3
"""Visualize a single glyph. Usage: python visualize_one.py <letter>"""

import sys
import importlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path
from fontTools.pens.recordingPen import RecordingPen

sys.path.insert(0, "src")
from config import FontConfig as fc
from glyph import Glyph

STROKE = 60


def recording_to_mpl_path(recording):
    """Convert RecordingPen operations to a matplotlib Path."""
    verts = []
    codes = []
    for op, args in recording.value:
        if op == "moveTo":
            verts.append(args[0])
            codes.append(Path.MOVETO)
        elif op == "lineTo":
            verts.append(args[0])
            codes.append(Path.LINETO)
        elif op == "curveTo":
            for pt in args:
                verts.append(pt)
            codes.extend([Path.CURVE4, Path.CURVE4, Path.CURVE4])
        elif op == "closePath":
            verts.append(verts[-len(verts) + codes.index(Path.MOVETO)])
            codes.append(Path.CLOSEPOLY)
    return Path(verts, codes)


def plot_control_points(ax, recording):
    """Plot on-curve points and off-curve control points with connecting lines."""
    for op, args in recording.value:
        if op == "moveTo":
            ax.plot(*args[0], "o", color="#2ecc71", markersize=5, zorder=5)
        elif op == "lineTo":
            ax.plot(*args[0], "o", color="#2ecc71", markersize=5, zorder=5)
        elif op == "curveTo":
            cp1, cp2, pt = args
            ax.plot(*cp1, "x", color="#e74c3c", markersize=6, zorder=5)
            ax.plot(*cp2, "x", color="#e74c3c", markersize=6, zorder=5)
            ax.plot(*pt, "o", color="#2ecc71", markersize=5, zorder=5)
            # Lines from on-curve to off-curve handles
            ax.plot([cp1[0], cp2[0]], [cp1[1], cp2[1]],
                    "-", color="#e74c3c", linewidth=0.5, alpha=0.5, zorder=4)


COLORS = ["#222222", "#e74c3c", "#3498db", "#2ecc71", "#e67e22", "#9b59b6", "#1abc9c"]


def visualize(family, glyph, show_controls=False, strokes=None):
    if strokes is None:
        strokes = [STROKE]

    mod = importlib.import_module(f"glyphs.{family}.{glyph}")
    glyph_cls = None
    for attr in vars(mod).values():
        if isinstance(attr, type) and issubclass(attr, Glyph) and attr is not Glyph:
            glyph_cls = attr
            break
    draw_fn = glyph_cls().draw

    fig, ax = plt.subplots(1, 1, figsize=(6, 8))

    for i, stroke in enumerate(sorted(strokes, reverse=True)):
        rec = RecordingPen()
        draw_fn(rec, stroke=stroke)
        path = recording_to_mpl_path(rec)
        color = COLORS[i % len(COLORS)]
        patch = mpatches.PathPatch(path, facecolor=color, edgecolor="none", alpha=0.7)
        ax.add_patch(patch)

        if show_controls:
            plot_control_points(ax, rec)

    # draw guides
    for y, label, color in [
        (0, "baseline", "#e74c3c"),
        (fc.x_height, "x-height", "#3498db"),
        (fc.cap, "cap", "#2ecc71"),
        (fc.descent, "descent", "#e67e22"),
        (fc.ascent, "ascent", "#9b59b6"),
    ]:
        ax.axhline(y, color=color, linewidth=0.5, linestyle="--", alpha=0.6)
        ax.text(fc.width + 10, y, label, fontsize=7, color=color, va="center")

    # advance width
    ax.axvline(0, color="#aaa", linewidth=0.5, linestyle=":")
    ax.axvline(fc.width, color="#aaa", linewidth=0.5, linestyle=":")

    ax.set_xlim(-50, fc.width + 80)
    ax.set_ylim(fc.descent - 50, fc.ascent + 50)
    ax.set_aspect("equal")
    ax.set_title(f"'{glyph}'", fontsize=16)
    ax.grid(True, alpha=0.15)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Visualize a single glyph")
    parser.add_argument("family", help="Glyph family (e.g. base, letters)")
    parser.add_argument("glyph", help="Glyph name (e.g. d, superellipse_ear)")
    parser.add_argument("-c", action="store_true", help="Show bezier control points")
    parser.add_argument("-s", type=str, default="60", help="Stroke width(s), comma-separated (e.g. 100,60,80)")
    args = parser.parse_args()
    strokes = [int(s) for s in args.s.split(",")]
    visualize(args.family, args.glyph, show_controls=args.c, strokes=strokes)
