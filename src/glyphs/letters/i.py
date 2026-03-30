from config import FontConfig as fc
from shapes.rect import draw_rect


def draw_i(
    pen,
    stroke: int,
):
    xmid = fc.width / 2 + fc.i_offset
    # Stem
    draw_rect(pen, xmid - stroke / 2, 0, xmid + stroke / 2, fc.x_height)
    # Footer
    draw_rect(
        pen,
        xmid - fc.i_len_left - stroke / 2,
        0,
        xmid + fc.i_len_right + stroke / 2,
        stroke,
    )
    # Left cap
    draw_rect(
        pen,
        xmid - fc.i_len_cap - stroke / 2,
        fc.x_height - stroke,
        xmid,
        fc.x_height,
    )
    # Accent dot
    draw_rect(
        pen,
        xmid - fc.i_dot_width - stroke / 2,
        fc.accent - fc.i_dot_width / 2 - stroke / 2,
        xmid + stroke / 2,
        fc.accent + stroke / 2 + fc.i_dot_width / 2,
    )
