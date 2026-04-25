import ufoLib2
from booleanOperations.booleanGlyph import BooleanGlyph

from shapes.superellipse import Superellipse
from draw.rect import draw_rect


def draw_arch(
    pen,
    stroke_x,
    stroke_y,
    x1,
    y1,
    x2,
    y2,
    hx,
    hy,
    side="right",
    cut=None,
    taper=0.5,
):
    w, h = (x2 - x1) / 2, (y2 - y1) / 2
    y_mid = y1 + h

    offset_x = taper * stroke_x
    offset_y = taper * stroke_y

    se = Superellipse(x1=x1, y1=y1, x2=x2, y2=y2, hx=hx, hy=hy)

    # Outer box
    outer_se = se.reduce(
        right=stroke_x - offset_x if side == "right" else 0,
        left=stroke_x - offset_x if side == "left" else 0,
        top=stroke_y - offset_y if side == "top" else 0,
        bottom=stroke_y - offset_y if side == "bottom" else 0,
    )
    inner_se = outer_se.reduce(
        left=stroke_x if side != "left" else offset_x,
        right=stroke_x if side != "right" else offset_x,
        top=stroke_y if side != "top" else offset_y,
        bottom=stroke_y if side != "bottom" else offset_y,
    )

    loop_glyph = ufoLib2.objects.Glyph()
    outer_se.draw(loop_glyph.getPen(), clockwise=False)
    inner_se.draw(loop_glyph.getPen(), clockwise=True)

    cuts = str(cut).split(",")
    cut_glyph = ufoLib2.objects.Glyph()
    cut_pen = cut_glyph.getPen()

    if "m_junction" in cuts:
        # First cut the bottom part
        draw_rect(cut_glyph.getPen(), x1 - 10, y1, x2 + 10, y_mid)
        result_1 = BooleanGlyph(loop_glyph).difference(BooleanGlyph(cut_glyph))

        # Cut the part after x2-offset
        cut_glyph = ufoLib2.objects.Glyph()
        draw_rect(cut_glyph.getPen(), x2 - offset_x, y1, x2 + 10, y2)
        result_2 = result_1.difference(BooleanGlyph(cut_glyph))

        result_2.draw(pen)
        
    else:
        if "bottom" in cuts:
            draw_rect(cut_pen, x1 - 10, y1, x2 + 10, y_mid)

        if "top" in cuts:
            draw_rect(cut_pen, x1 - 10, y_mid, x2 + 10, y2)

        if "left" in cuts:
            x_mid = x1 + w
            draw_rect(cut_pen, x1, y1 - 10, x_mid, y2 + 10)

        if "right" in cuts:
            x_mid = x1 + w
            draw_rect(cut_pen, x_mid, y1 - 10, x2, y2 + 10)

        result = BooleanGlyph(loop_glyph).difference(BooleanGlyph(cut_glyph))
        result.draw(pen)

    return {
        "offset_x": offset_x,
        "offset_y": offset_y,
        "outer": outer_se,
        "inner": inner_se,
    }
