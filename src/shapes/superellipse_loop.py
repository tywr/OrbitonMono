from shapes.superellipse import draw_superellipse


def draw_superellipse_loop(
    pen,
    stroke_x,
    stroke_y,
    x1,
    y1,
    x2,
    y2,
    hx,
    hy,
    cut=None,
):
    w = (x2 - x1) / 2
    h = (y2 - y1) / 2
    inner_hx = hx * (w - stroke_x) / w
    inner_hy = hy * (h - stroke_y) / h

    draw_superellipse(pen, x1, y1, x2, y2, hx, hy, clockwise=False, cut=cut)

    draw_superellipse(
        pen,
        x1 + stroke_x,
        y1 + stroke_y,
        x2 - stroke_x,
        y2 - stroke_y,
        inner_hx,
        inner_hy,
        clockwise=True,
        cut=cut,
    )
