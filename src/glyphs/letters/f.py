from config import FontConfig as fc
from shapes.corner import draw_corner
from shapes.rect import draw_rect


def draw_f(
    pen,
    stroke: int,
):
    xmid = fc.width / 2 + fc.f_offset
    # Stem
    draw_rect(pen, xmid - stroke / 2, 0, xmid + stroke / 2, fc.x_height)
    # Cross-bar
    draw_rect(
        pen,
        xmid - fc.f_len_left - stroke / 2,
        fc.bar_height - stroke,
        xmid + fc.f_len_right + stroke / 2,
        fc.bar_height,
    )
    # Corner
    draw_corner(
        pen,
        stroke,
        xmid - stroke / 2,
        fc.x_height,
        xmid + fc.f_corner_width,
        fc.ascent,
        fc.f_hx,
        fc.f_hy,
        orientation="top-right",
    )
    # Extension after the corner to the right
    if fc.f_len_right > fc.f_corner_width:
        draw_rect(
            pen,
            xmid + fc.f_corner_width,
            fc.ascent - stroke,
            xmid + fc.f_len_right + stroke / 2,
            fc.ascent,
        )
