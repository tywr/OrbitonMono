class Superellipse:
    __slots__ = ("x1", "y1", "x2", "y2", "hx", "hy")

    def __init__(self, x1, y1, x2, y2, hx, hy):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.hx = hx
        self.hy = hy

    def translate(self, dx=0, dy=0):
        return Superellipse(
            self.x1 + dx,
            self.y1 + dy,
            self.x2 + dx,
            self.y2 + dy,
            self.hx,
            self.hy,
        )


def draw_superellipse(
    pen,
    x1,
    y1,
    x2,
    y2,
    hx,
    hy,
    clockwise=False,
    cut=None,
):
    """
    Draw a superellipse whose anchors sit at the midpoint of each bounding side.

    Starting the drawing on the right side of the drawing.

    Args:
        x1, y1: bottom-left corner of the bounding box.
        x2, y2: top-right corner of the bounding box.
        hx: horizontal handle offset from the side midpoint anchor.
        hy: vertical handle offset from the side midpoint anchor.
        clockwise: winding direction (True for inner contour / counter).
        cut: optional cut side ("top", "bottom", "left", "right") to draw
             only the opposite half of the superellipse.
    """
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2

    if clockwise:
        # Winding: left → top → right → bottom → left
        if cut is None:
            pen.moveTo((x1, mid_y))
            pen.curveTo((x1, mid_y + hy), (mid_x - hx, y2), (mid_x, y2))
            pen.curveTo((mid_x + hx, y2), (x2, mid_y + hy), (x2, mid_y))
            pen.curveTo((x2, mid_y - hy), (mid_x + hx, y1), (mid_x, y1))
            pen.curveTo((mid_x - hx, y1), (x1, mid_y - hy), (x1, mid_y))
        elif cut == "top":
            pen.moveTo((x2, mid_y))
            pen.curveTo((x2, mid_y - hy), (mid_x + hx, y1), (mid_x, y1))
            pen.curveTo((mid_x - hx, y1), (x1, mid_y - hy), (x1, mid_y))
        elif cut == "bottom":
            pen.moveTo((x1, mid_y))
            pen.curveTo((x1, mid_y + hy), (mid_x - hx, y2), (mid_x, y2))
            pen.curveTo((mid_x + hx, y2), (x2, mid_y + hy), (x2, mid_y))
        elif cut == "right":
            pen.moveTo((mid_x, y1))
            pen.curveTo((mid_x - hx, y1), (x1, mid_y - hy), (x1, mid_y))
            pen.curveTo((x1, mid_y + hy), (mid_x - hx, y2), (mid_x, y2))
        elif cut == "left":
            pen.moveTo((mid_x, y2))
            pen.curveTo((mid_x + hx, y2), (x2, mid_y + hy), (x2, mid_y))
            pen.curveTo((x2, mid_y - hy), (mid_x + hx, y1), (mid_x, y1))
    else:
        # Winding: right → top → left → bottom → right
        if cut is None:
            pen.moveTo((x2, mid_y))
            pen.curveTo((x2, mid_y + hy), (mid_x + hx, y2), (mid_x, y2))
            pen.curveTo((mid_x - hx, y2), (x1, mid_y + hy), (x1, mid_y))
            pen.curveTo((x1, mid_y - hy), (mid_x - hx, y1), (mid_x, y1))
            pen.curveTo((mid_x + hx, y1), (x2, mid_y - hy), (x2, mid_y))
        elif cut == "top":
            pen.moveTo((x1, mid_y))
            pen.curveTo((x1, mid_y - hy), (mid_x - hx, y1), (mid_x, y1))
            pen.curveTo((mid_x + hx, y1), (x2, mid_y - hy), (x2, mid_y))
        elif cut == "bottom":
            pen.moveTo((x2, mid_y))
            pen.curveTo((x2, mid_y + hy), (mid_x + hx, y2), (mid_x, y2))
            pen.curveTo((mid_x - hx, y2), (x1, mid_y + hy), (x1, mid_y))
        elif cut == "right":
            pen.moveTo((mid_x, y2))
            pen.curveTo((mid_x - hx, y2), (x1, mid_y + hy), (x1, mid_y))
            pen.curveTo((x1, mid_y - hy), (mid_x - hx, y1), (mid_x, y1))
        elif cut == "left":
            pen.moveTo((mid_x, y1))
            pen.curveTo((mid_x + hx, y1), (x2, mid_y - hy), (x2, mid_y))
            pen.curveTo((x2, mid_y + hy), (mid_x + hx, y2), (mid_x, y2))

    pen.closePath()

    return Superellipse(x1, y1, x2, y2, hx, hy)
