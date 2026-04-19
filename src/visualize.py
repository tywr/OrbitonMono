#!/usr/bin/env python3
"""Visualize a single glyph (by slug name) or a text string."""

import sys
import argparse
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path
import pathops
from fontTools.pens.recordingPen import RecordingPen

sys.path.insert(0, "src")
from config import FontConfig as fc
from config import DrawConfig
from glyphs import LigatureGlyph
from generate_font import discover_glyphs


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
            ax.plot(
                [cp1[0], cp2[0]],
                [cp1[1], cp2[1]],
                "-",
                color="#e74c3c",
                linewidth=0.5,
                alpha=0.5,
                zorder=4,
            )


COLORS = ["#222222", "#e74c3c", "#3498db", "#2ecc71", "#e67e22", "#9b59b6", "#1abc9c"]


def _flatten_bezier(p0, p1, p2, p3, n=16):
    """Sample a cubic bezier into n line segments."""
    pts = []
    for i in range(1, n + 1):
        t = i / n
        u = 1 - t
        x = u**3 * p0[0] + 3 * u**2 * t * p1[0] + 3 * u * t**2 * p2[0] + t**3 * p3[0]
        y = u**3 * p0[1] + 3 * u**2 * t * p1[1] + 3 * u * t**2 * p2[1] + t**3 * p3[1]
        pts.append((x, y))
    return pts


def compute_optical_center(recording):
    """Compute area-weighted centroid from RecordingPen operations."""
    contours = []
    current = []
    for op, args in recording.value:
        if op == "moveTo":
            current = [args[0]]
        elif op == "lineTo":
            current.append(args[0])
        elif op == "curveTo":
            prev = current[-1]
            current.extend(_flatten_bezier(prev, args[0], args[1], args[2]))
        elif op == "closePath":
            if current:
                contours.append(current)
                current = []

    total_area = 0
    cx_sum = 0
    cy_sum = 0
    for pts in contours:
        n = len(pts)
        a = 0
        sx = 0
        sy = 0
        for i in range(n):
            j = (i + 1) % n
            cross = pts[i][0] * pts[j][1] - pts[j][0] * pts[i][1]
            a += cross
            sx += (pts[i][0] + pts[j][0]) * cross
            sy += (pts[i][1] + pts[j][1]) * cross
        a *= 0.5
        if abs(a) < 1e-6:
            continue
        sx /= 6 * a
        sy /= 6 * a
        total_area += a
        cx_sum += sx * a
        cy_sum += sy * a

    if abs(total_area) < 1e-6:
        return None
    return cx_sum / total_area, cy_sum / total_area


def find_glyph(slug_name, all_glyphs):
    for g in all_glyphs:
        if g.name == slug_name:
            return g
    raise SystemExit(f"No glyph found with name '{slug_name}'")


def visualize_glyph(slug_name, show_controls=False, show_optical_center=False, configs=None):
    if configs is None:
        configs = [DrawConfig()]

    glyph_inst = find_glyph(slug_name, discover_glyphs())
    draw_fn = glyph_inst.draw
    n_chars = glyph_inst.number_characters
    total_width = fc.window_width * n_chars

    fig, ax = plt.subplots(1, 1, figsize=(3 + 3 * n_chars, 8))

    for i, dc in enumerate(configs):
        rec = RecordingPen()
        draw_fn(rec, dc=dc)
        path = recording_to_mpl_path(rec)
        color = COLORS[i % len(COLORS)]
        patch = mpatches.PathPatch(path, facecolor=color, edgecolor="none", alpha=0.7)
        ax.add_patch(patch)

        if show_controls:
            plot_control_points(ax, rec)

    if show_optical_center:
        rec = RecordingPen()
        draw_fn(rec, dc=configs[0])
        center = compute_optical_center(rec)
        if center:
            ax.plot(
                *center,
                "+",
                color="#e74c3c",
                markersize=20,
                markeredgewidth=3,
                zorder=10,
            )
            ax.annotate(
                f"({center[0]:.0f}, {center[1]:.0f})",
                xy=center,
                xytext=(12, -12),
                textcoords="offset points",
                fontsize=9,
                color="#e74c3c",
                fontweight="bold",
            )

    for y, label, color in [
        (0, "baseline", "#e74c3c"),
        (fc.x_height, "x-height", "#3498db"),
        (fc.cap, "cap", "#2ecc71"),
        (fc.descent, "descent", "#e67e22"),
        (fc.ascent, "ascent", "#9b59b6"),
    ]:
        ax.axhline(y, color=color, linewidth=0.5, linestyle="--", alpha=0.6)
        ax.text(total_width + 10, y, label, fontsize=7, color=color, va="center")

    ax.axvline(0, color="#555", linewidth=1.5, linestyle="-")
    ax.axvline(total_width, color="#555", linewidth=1.5, linestyle="-")
    for i in range(1, n_chars):
        ax.axvline(i * fc.window_width, color="#555", linewidth=0.8, linestyle=":")
    ax.axhline(fc.window_descent, color="#555", linewidth=1.5, linestyle="-")
    ax.axhline(fc.window_ascent, color="#555", linewidth=1.5, linestyle="-")

    ax.set_xlim(-50, total_width + 80)
    ax.set_ylim(fc.window_descent - 50, fc.window_ascent + 50)
    ax.set_aspect("equal")
    ax.set_title(f"'{slug_name}'", fontsize=16)
    plt.tight_layout()
    plt.show()


def visualize_text(text, point_size=None, guides=False, dc=None):
    if dc is None:
        dc = DrawConfig()
    all_glyphs = discover_glyphs()

    glyph_map = {}
    for g in all_glyphs:
        if g.unicode and not g.font_feature:
            char = chr(int(g.unicode, 16))
            glyph_map[char] = g

    ligature_map = {}
    for g in all_glyphs:
        if not isinstance(g, LigatureGlyph):
            continue
        seq = ""
        for comp_name in g.components:
            for og in all_glyphs:
                if og.name == comp_name and og.unicode:
                    seq += chr(int(og.unicode, 16))
                    break
        if len(seq) == len(g.components):
            ligature_map[seq] = g
    ligatures = sorted(ligature_map.keys(), key=len, reverse=True)

    fig, ax = plt.subplots(1, 1, figsize=(max(6, len(text) * 1.5), 4), dpi=200)

    cursor_x = 0
    i = 0
    while i < len(text):
        glyph = None
        consumed = 1
        for seq in ligatures:
            if text[i:i + len(seq)] == seq:
                glyph = ligature_map[seq]
                consumed = len(seq)
                break

        if glyph is None:
            ch = text[i]
            if ch == " ":
                cursor_x += fc.window_width
                i += 1
                continue
            glyph = glyph_map.get(ch)
            if glyph is None:
                cursor_x += fc.window_width
                i += 1
                continue

        raw_path = pathops.Path()
        glyph.draw(pathops.PathPen(raw_path), dc=dc)
        simplified = pathops.simplify(
            raw_path, clockwise=False, keep_starting_points=True
        )

        rec = RecordingPen()
        simplified.draw(rec)

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

        cursor_x += fc.window_width * glyph.number_characters
        i += consumed

    if guides:
        for i in range(len(text) + 1):
            x = i * fc.window_width
            ax.axvline(x, color="#aaa", linewidth=0.5, linestyle=":")

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

    if point_size is not None:
        ipu = point_size / (72 * fc.units_per_em)

        def _apply_fixed_scale(event=None):
            fig_w, fig_h = fig.get_size_inches()
            ax_pos = ax.get_position()
            ax_w = fig_w * ax_pos.width
            ax_h = fig_h * ax_pos.height
            units_w = ax_w / ipu
            units_h = ax_h / ipu
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
    parser = argparse.ArgumentParser(
        description="Visualize a Kassiopea glyph (by slug name) or a text string"
    )
    parser.add_argument(
        "slug",
        nargs="?",
        help="Glyph slug name (e.g. lowercase_o). Ignored when -t is used.",
    )
    parser.add_argument("-t", "--text", type=str, default=None, help="Render a text string")
    parser.add_argument("-c", action="store_true", help="Show bezier control points (construction)")
    parser.add_argument("-o", action="store_true", help="Show optical center")
    parser.add_argument(
        "-s",
        type=str,
        default="regular",
        help="Style: 'regular', 'bold', 'italic', or comma-separated stroke widths",
    )
    parser.add_argument("--pt", type=float, default=None, help="Point size (text mode)")
    parser.add_argument("--guides", action="store_true", help="Show helper lines (text mode)")
    args = parser.parse_args()

    style = args.s.strip().lower()
    if style == "regular":
        configs = [DrawConfig()]
    elif style == "bold":
        configs = [DrawConfig.weight(w=700)]
    elif style == "italic":
        configs = [DrawConfig.italic()]
    else:
        configs = [
            DrawConfig(stroke_x=int(s), stroke_y=int(s) - 10)
            for s in args.s.split(",")
        ]

    if args.text is not None:
        visualize_text(
            args.text,
            point_size=args.pt,
            guides=args.guides,
            dc=configs[0],
        )
    else:
        if not args.slug:
            parser.error("Provide a glyph slug name (e.g. lowercase_o) or use -t TEXT")
        visualize_glyph(
            args.slug,
            show_controls=args.c,
            show_optical_center=args.o,
            configs=configs,
        )
