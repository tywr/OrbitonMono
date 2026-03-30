from config import FontConfig as fc
from shapes.superellipse_loop import draw_superellipse_loop
from shapes.corner import draw_corner
from shapes.rect import draw_rect


def draw_e(
    pen,
    stroke: int,
):
    x1 = fc.width / 2 - fc.o_width / 2 - stroke / 2
    y1 = -fc.overshoot
    x2 = fc.width / 2 + fc.o_width / 2 + stroke / 2
    y2 = fc.x_height + fc.overshoot
    ymid = y1 + (y2 - y1) / 2
    xmid = x1 + (x2 - x1) / 2

    # Half-top of a superellipse
    draw_superellipse_loop(pen, stroke, x1, y1, x2, y2, fc.o_hx, fc.o_hy, cut="bottom")
    # Corner from mid-left to bottom
    draw_corner(
        pen,
        stroke,
        x1,
        (fc.x_height + 2 * fc.overshoot) / 2 + fc.overshoot,
        xmid,
        0,
        fc.o_hx,
        fc.o_hy,
        orientation="bottom-right",
    )
    # Extension
    draw_rect(pen, xmid, 0, x2 - stroke / 2, stroke)
    # Mid-bar
    draw_rect(pen, x1 + stroke / 2, ymid, x2 - stroke / 2, ymid + stroke / 2)
    draw_rect(pen, x1 + stroke / 2, ymid - stroke / 2, x2, ymid)
