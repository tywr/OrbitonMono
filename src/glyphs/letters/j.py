from config import FontConfig as fc
from shapes.corner import draw_corner
from shapes.rect import draw_rect


def draw_j(
    pen,
    stroke: int,
):
    xmid = fc.width / 2 + fc.j_offset
    draw_rect(pen, xmid - stroke / 2, 0, xmid + stroke / 2, fc.x_height)
    draw_rect(
        pen,
        xmid - fc.i_len_cap - stroke / 2,
        fc.x_height - stroke,
        xmid,
        fc.x_height,
    )
    draw_rect(
        pen,
        xmid - fc.i_dot_width - stroke / 2,
        fc.accent - fc.i_dot_width / 2 - stroke / 2,
        xmid + stroke / 2,
        fc.accent + stroke / 2 + fc.i_dot_width / 2,
    )
    draw_corner(
        pen,
        stroke,
        xmid + stroke / 2,
        0,
        xmid - fc.j_corner_width,
        fc.descent + fc.tail_offset,
        fc.j_hx,
        fc.j_hy,
        orientation="bottom-left",
    )
    if fc.j_len_left > fc.j_corner_width:
        draw_rect(
            pen,
            xmid - fc.j_len_left - stroke / 2,
            fc.descent + fc.tail_offset,
            xmid - fc.j_corner_width,
            fc.descent + fc.tail_offset + stroke,
        )
