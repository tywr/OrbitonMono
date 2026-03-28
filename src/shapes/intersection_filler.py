from shapes.rect import rect
from shapes.intersect import rounded_rect_intersect_x


def fill_intersection(
    pen,
    stroke: float,
    direction: str,
    side: str,
    x: float,
    y: float,
    fill_height: float,
):
    print(x, y)
    x1 = x - stroke / 2
    x2 = x + stroke / 2
    if direction == "bottom":
        y1 = y - fill_height
        y2 = y
    if direction == "top":
        y1 = y
        y2 = y + fill_height
    rect(pen, x1, y1, x2, y2)


def intersection_filler(
    pen,
    stroke,
    outer_left,
    outer_right,
    height,
    x_offset,
    y_offset,
    bar_left,
    fill_height,
):
    hits = rounded_rect_intersect_x(
        outer_left,
        0,
        outer_right,
        height,
        x_offset,
        y_offset,
        bar_left,
    )

    if len(hits) >= 2:
        bottom, top = hits[0], hits[-1]
        print(hits)
        fill_intersection(
            pen,
            stroke=stroke,
            direction="bottom",
            side="right",
            x=bottom[0],
            y=bottom[1],
            fill_height=fill_height,
        )
        fill_intersection(
            pen,
            stroke=stroke,
            direction="top",
            side="right",
            x=top[0],
            y=top[1],
            fill_height=fill_height,
        )
