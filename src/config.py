class FontConfig:
    family_name = "Kassiopea"

    units_per_em = 1000
    window_ascent = 1020
    window_descent = -300
    ascent = 730
    descent = -200
    cap = 730
    width = 600
    x_height = 550
    accent = 645
    overshoot = 10
    h_overshoot = 5

    # Standard hx and hy curve parameters for superellipse
    hx = 200
    hy = 200

    # Alternative hx and hy for letters like a, u, n, h
    a_ratio = 0.6
    a_hx = hx * 0.8
    a_hy = hy * 0.6

    # Depth of tooth
    tooth = 68

    # Amount of tooth gap coverage
    gap = 5
    cover = 10

    # Y-axis offset of the tail above descender line (g, y)
    tail_offset = 20

    # Standard width of characters
    body_width = 340


    # Curve parameter for ear
    ehy = 30
