#!/usr/bin/env python3
"""Compute the distance between the right side of one glyph and the left side of another.

Usage: python -m distance lowercase_o lowercase_i
"""

import argparse

import pathops
from fontTools.pens.boundsPen import BoundsPen

from config import FontConfig as fc, DrawConfig
from generate_font import discover_glyphs


def glyph_bounds(glyph):
    """Return (xMin, yMin, xMax, yMax) of a glyph's simplified outline."""
    path = pathops.Path()
    glyph.draw(pathops.PathPen(path), dc=DrawConfig())
    simplified = pathops.simplify(path, clockwise=False, keep_starting_points=True)

    pen = BoundsPen(None)
    simplified.draw(pen)
    return pen.bounds  # (xMin, yMin, xMax, yMax)


def main():
    parser = argparse.ArgumentParser(description="Distance between two glyphs")
    parser.add_argument("left", help="Name of the left glyph (e.g. lowercase_o)")
    parser.add_argument("right", help="Name of the right glyph (e.g. lowercase_i)")
    args = parser.parse_args()

    all_glyphs = discover_glyphs()
    by_name = {g.name: g for g in all_glyphs}

    if args.left not in by_name:
        print(f"Unknown glyph: {args.left}")
        return
    if args.right not in by_name:
        print(f"Unknown glyph: {args.right}")
        return

    left_bounds = glyph_bounds(by_name[args.left])
    right_bounds = glyph_bounds(by_name[args.right])

    right_gap = fc.window_width - left_bounds[2]   # window_width - xMax
    left_gap = right_bounds[0]                      # xMin

    print(f"{args.left}  right edge: {left_bounds[2]:.0f}  gap to cell wall: {right_gap:.0f}")
    print(f"{args.right}  left edge:  {right_bounds[0]:.0f}  gap to cell wall: {left_gap:.0f}")
    print(f"distance: {right_gap + left_gap:.0f}")


if __name__ == "__main__":
    main()
