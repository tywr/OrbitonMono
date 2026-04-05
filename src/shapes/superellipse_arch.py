import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph

from shapes.rect import draw_rect
from shapes.superellipse import Superellipse, draw_superellipse
from utils.intersection import find_offset


def draw_superellipse_arch(
    pen,
    stroke_x,
    stroke_y,
    x1,
    y1,
    x2,
    y2,
    hx,
    hy,
    dent=70,
    side="right",
    cut=None,
    offset=None,
):
    w, h = (x2 - x1) / 2, (y2 - y1) / 2
    y_mid = y1 + h

    if offset is None:
        if side in ("left", "right"):
            offset = find_offset(x1, y1, x2, y2, hx, hy, stroke_x, dent)
        else:
            offset = find_offset(-y2, x1, -y1, x2, hy, hx, stroke_y, dent)

    # Outer box
    ox1 = x1 + (stroke_x - offset if side == "left" else 0)
    oy1 = y1 + (stroke_y - offset if side == "bottom" else 0)
    ox2 = x2 - (stroke_x - offset if side == "right" else 0)
    oy2 = y2 - (stroke_y - offset if side == "top" else 0)
    ohx = hx * (w - offset) / w
    ohy = hy * (h - offset) / h

    ihx = hx * (w - stroke_x) / w
    ihy = hy * (h - stroke_y) / h

    # Inner box
    ix1 = x1 + stroke_x
    iy1 = y1 + stroke_y
    ix2 = x2 - stroke_x
    iy2 = y2 - stroke_y

    loop_glyph = ufoLib2.objects.Glyph()
    draw_superellipse(
        loop_glyph.getPen(), ox1, oy1, ox2, oy2, ohx, ohy, clockwise=False
    )
    draw_superellipse(loop_glyph.getPen(), ix1, iy1, ix2, iy2, ihx, ihy, clockwise=True)

    if cut == "bottom":
        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(cut_glyph.getPen(), x1 - 10, y1, x2 + 10, y_mid)
        result = BooleanGlyph(loop_glyph).difference(BooleanGlyph(cut_glyph))
        result.draw(pen)

    elif cut == "top":
        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(cut_glyph.getPen(), x1 - 10, y_mid, x2 + 10, y2)
        result = BooleanGlyph(loop_glyph).difference(BooleanGlyph(cut_glyph))
        result.draw(pen)

    elif cut == "left":
        x_mid = x1 + w
        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(cut_glyph.getPen(), x1, y1 - 10, x_mid, y2 + 10)
        result = BooleanGlyph(loop_glyph).difference(BooleanGlyph(cut_glyph))
        result.draw(pen)

    elif cut == "right":
        x_mid = x1 + w
        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(cut_glyph.getPen(), x_mid, y1 - 10, x2, y2 + 10)
        result = BooleanGlyph(loop_glyph).difference(BooleanGlyph(cut_glyph))
        result.draw(pen)

    elif cut == "m_junction":
        # First cut the bottom part
        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(cut_glyph.getPen(), x1 - 10, y1, x2 + 10, y_mid)
        result_1 = BooleanGlyph(loop_glyph).difference(BooleanGlyph(cut_glyph))

        # Cut the part after x2-offset
        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(cut_glyph.getPen(), x2 - offset, y1, x2 + 10, y2)
        result_2 = result_1.difference(BooleanGlyph(cut_glyph))

        result_2.draw(pen)

    else:
        result = BooleanGlyph(loop_glyph)
        result.draw(pen)

    return {
        "offset": offset,
        "outer": Superellipse(
            x1=ox1,
            y1=oy1,
            x2=ox2,
            y2=oy2,
            hx=ohx,
            hy=ohy,
        ),
        "inner": Superellipse(
            x1=ix1,
            y1=iy1,
            x2=ix2,
            y2=iy2,
            hx=ihx,
            hy=ihy,
        ),
    }
