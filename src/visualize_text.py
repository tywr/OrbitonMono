#!/usr/bin/env python3
"""Visualize a text string using Kassiopea glyphs.

Usage: python -m visualize_text "Lorem ipsum"
"""

import sys
import argparse

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pathops
from fontTools.pens.recordingPen import RecordingPen

sys.path.insert(0, "src")
from config import FontConfig as fc
from generate_font import discover_glyphs, STROKE

from visualize import recording_to_mpl_path


def visualize_text(text, stroke=STROKE):
    all_glyphs = discover_glyphs()
    glyph_map = {}
    for g in all_glyphs:
        char = chr(int(g.unicode, 16))
        glyph_map[char] = g

    fig, ax = plt.subplots(1, 1, figsize=(max(6, len(text) * 1.5), 4))

    cursor_x = 0
    for ch in text:
        if ch == " ":
            cursor_x += fc.width
            continue

        glyph = glyph_map.get(ch)
        if glyph is None:
            cursor_x += fc.width
            continue

        # Draw through pathops to get simplified/correct winding
        raw_path = pathops.Path()
        glyph.draw(pathops.PathPen(raw_path), stroke=stroke)
        simplified = pathops.simplify(raw_path, clockwise=False, keep_starting_points=True)

        # Record the simplified path
        rec = RecordingPen()
        simplified.draw(rec)

        # Offset all points by cursor_x
        offset_ops = []
        for op, args in rec.value:
            if op == "closePath" or op == "endPath":
                offset_ops.append((op, args))
            else:
                offset_ops.append((op, tuple((x + cursor_x, y) for x, y in args)))
        rec.value = offset_ops

        path = recording_to_mpl_path(rec)
        patch = mpatches.PathPatch(path, facecolor="#222222", edgecolor="none")
        ax.add_patch(patch)

        cursor_x += fc.width

    # Vertical cell separators
    for i in range(len(text) + 1):
        x = i * fc.width
        ax.axvline(x, color="#aaa", linewidth=0.5, linestyle=":")

    # Guides
    for y, label, color in [
        (0, "baseline", "#e74c3c"),
        (fc.x_height, "x-height", "#3498db"),
        (fc.ascent, "ascent", "#9b59b6"),
        (fc.descent, "descent", "#e67e22"),
    ]:
        ax.axhline(y, color=color, linewidth=0.5, linestyle="--", alpha=0.6)
        ax.text(cursor_x + 10, y, label, fontsize=7, color=color, va="center")

    ax.set_xlim(-50, cursor_x + 80)
    ax.set_ylim(fc.descent - 50, fc.ascent + 50)
    ax.set_aspect("equal")
    ax.set_title(text, fontsize=14)
    ax.grid(True, alpha=0.15)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize text with Kassiopea font")
    parser.add_argument("text", help="Text string to render")
    parser.add_argument("-s", type=int, default=STROKE, help="Stroke width")
    args = parser.parse_args()
    visualize_text(args.text, stroke=args.s)
