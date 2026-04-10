#!/usr/bin/env python3
"""Visualize a text string using Kassiopea glyphs.

Usage: python -m visualize_text "Lorem ipsum" [--pt 18]
"""

import sys
import argparse

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pathops
from fontTools.pens.recordingPen import RecordingPen

sys.path.insert(0, "src")
from config import FontConfig as fc
from config import DrawConfig
from generate_font import discover_glyphs

from visualize import recording_to_mpl_path


def visualize_text(text, point_size=None, guides=False):
    all_glyphs = discover_glyphs()
    glyph_map = {}
    for g in all_glyphs:
        if g.unicode:
            char = chr(int(g.unicode, 16))
            glyph_map[char] = g

    fig, ax = plt.subplots(1, 1, figsize=(max(6, len(text) * 1.5), 4), dpi=200)

    cursor_x = 0
    for ch in text:
        if ch == " ":
            cursor_x += fc.window_width
            continue

        glyph = glyph_map.get(ch)
        if glyph is None:
            cursor_x += fc.window_width
            continue

        # Draw through pathops to get simplified/correct winding
        raw_path = pathops.Path()
        glyph.draw(pathops.PathPen(raw_path), dc=DrawConfig())
        simplified = pathops.simplify(
            raw_path, clockwise=False, keep_starting_points=True
        )

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

        cursor_x += fc.window_width

    if guides:
        # Vertical cell separators
        for i in range(len(text) + 1):
            x = i * fc.window_width
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
    ax.set_ylim(fc.window_descent - 50, fc.window_ascent + 50)
    ax.set_aspect("equal")
    if point_size is not None:
        ax.set_title(f"{point_size}pt", fontsize=14)
    else:
        ax.set_title(text, fontsize=14)
    ax.set_axis_off()

    # When a point size is specified, lock the data-to-display ratio so the
    # glyphs stay at the requested physical size regardless of window resizing.
    if point_size is not None:
        # inches per font unit: at point_size pt, units_per_em units = point_size/72 inches
        ipu = point_size / (72 * fc.units_per_em)

        def _apply_fixed_scale(event=None):
            fig_w, fig_h = fig.get_size_inches()
            # Subtract space for title/margins (approximate)
            ax_pos = ax.get_position()
            ax_w = fig_w * ax_pos.width
            ax_h = fig_h * ax_pos.height
            # How many font units fit in the axes at this physical size
            units_w = ax_w / ipu
            units_h = ax_h / ipu
            # Center on the text content
            cx = cursor_x / 2
            cy = (fc.ascent + fc.descent) / 2
            ax.set_xlim(cx - units_w / 2, cx + units_w / 2)
            ax.set_ylim(cy - units_h / 2, cy + units_h / 2)
            fig.canvas.draw_idle()

        fig.canvas.mpl_connect("resize_event", _apply_fixed_scale)
        plt.tight_layout()
        _apply_fixed_scale()
    else:
        plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize text with Kassiopea font")
    parser.add_argument("text", help="Text string to render")
    parser.add_argument("--pt", type=float, default=None, help="Point size (e.g. 18)")
    parser.add_argument("--guides", action="store_true", help="Show helper lines")
    args = parser.parse_args()
    visualize_text(args.text, point_size=args.pt, guides=args.guides)
