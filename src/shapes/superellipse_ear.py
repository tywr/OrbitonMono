from shapes.rect import draw_rect


def draw_superellipse_ear(
    pen,
    stroke,
    x1,
    y1,
    x2,
    y2,
    hx,
    hy,
    tooth,
    cover,
    side="right",
    cut=None,
):
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2

    w = (x2 - x1) / 2
    h = (y2 - y1) / 2
    ihx = hx * (w - stroke) / w
    ihy = hy * (h - stroke) / h

    # Inner box
    ix1 = x1 + stroke
    iy1 = y1 + stroke
    ix2 = x2 - stroke
    iy2 = y2 - stroke
    imid_x = (ix1 + ix2) / 2
    imid_y = (iy1 + iy2) / 2

    if side == "left":
        # Junction on left side
        p_bot = (x1 + stroke, y1 + tooth - stroke / 2)
        p_top = (x1 + stroke, y2 - tooth + stroke / 2)
        junction_x = x1 + stroke

        if cut != "bottom":
            # Bottom half: p_bot → outer bottom → outer right mid → inner right mid → inner bottom → closePath
            pen.moveTo(p_bot)
            pen.curveTo((p_bot[0], y1), (mid_x, y1), (mid_x, y1))
            pen.curveTo((mid_x + hx, y1), (x2, mid_y - hy), (x2, mid_y))
            pen.lineTo((ix2, imid_y))
            pen.curveTo((ix2, imid_y - ihy), (imid_x + ihx, iy1), (imid_x, iy1))
            pen.curveTo((imid_x - ihx, iy1), (ix1, imid_y - ihy), (ix1, imid_y))
            pen.closePath()

        if cut != "top":
            # Top half: outer right mid → outer top → p_top → inner left mid → inner top → inner right mid → closePath
            pen.moveTo((x2, mid_y))
            pen.curveTo((x2, mid_y + hy), (mid_x + hx, y2), (mid_x, y2))
            pen.curveTo((p_top[0], y2), p_top, p_top)
            pen.lineTo((ix1, imid_y))
            pen.curveTo((ix1, imid_y + ihy), (imid_x - ihx, iy2), (imid_x, iy2))
            pen.curveTo((imid_x + ihx, iy2), (ix2, imid_y + ihy), (ix2, imid_y))
            pen.closePath()

    elif side == "right":
        # Junction on right side
        p_bot = (x2 - stroke, y1 + tooth - stroke / 2)
        p_top = (x2 - stroke, y2 - tooth + stroke / 2)
        junction_x = x2 - stroke

        if cut != "top":
            # Top half: p_top → outer top → outer left mid → inner left mid → inner top → closePath
            pen.moveTo(p_top)
            pen.curveTo((p_top[0], y2), (mid_x, y2), (mid_x, y2))
            pen.curveTo((mid_x - hx, y2), (x1, mid_y + hy), (x1, mid_y))
            pen.lineTo((ix1, imid_y))
            pen.curveTo((ix1, imid_y + ihy), (imid_x - ihx, iy2), (imid_x, iy2))
            pen.curveTo((imid_x + ihx, iy2), (ix2, imid_y + ihy), (ix2, imid_y))
            pen.closePath()

        if cut != "bottom":
            # Bottom half: outer left mid → outer bottom → p_bot → inner right mid → inner bottom → inner left mid → closePath
            pen.moveTo((x1, mid_y))
            pen.curveTo((x1, mid_y - hy), (mid_x - hx, y1), (mid_x, y1))
            pen.curveTo((mid_x, y1), (p_bot[0], y1), p_bot)
            pen.lineTo((ix2, imid_y))
            pen.curveTo((ix2, imid_y - ihy), (imid_x + ihx, iy1), (imid_x, iy1))
            pen.curveTo((imid_x - ihx, iy1), (ix1, imid_y - ihy), (ix1, imid_y))
            pen.closePath()

    # Draw the covers
    xl = junction_x if side == "left" else junction_x - stroke / 8
    xr = junction_x if side == "right" else junction_x + stroke / 8
    y_low = y1 + tooth - stroke / 2
    y_high = y2 - tooth + stroke / 2
    if cut != "bottom":
        draw_rect(pen, xl, y_low - cover, xr, y_low)
    if cut != "top":
        draw_rect(pen, xl, y_high, xr, y_high + cover)
