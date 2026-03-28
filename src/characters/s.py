import pathops

from config import FontConfig
from shapes.rounded_rect import rounded_rect


def draw_s(pen, font_config: FontConfig, stroke: int):
    """Draw a lowercase 's' — two stacked C-shapes, top opens right, bottom opens left."""
    outer_left = FontConfig.WIDTH / 2 - FontConfig.X_WIDTH / 2 - stroke / 2
    outer_right = FontConfig.WIDTH / 2 + FontConfig.X_WIDTH / 2 + stroke / 2
    mid_y = FontConfig.X_HEIGHT / 2
    top = FontConfig.X_HEIGHT

    h_radius = FontConfig.H_RADIUS
    v_radius = FontConfig.V_RADIUS

    # --- Top half: rounded rect from mid_y to top, opening on the right ---
    top_outer_cv = min(v_radius, (top - mid_y) / 2)
    top_outer_ch = min(h_radius, (outer_right - outer_left) / 2)

    top_shape = pathops.Path()
    top_pen = top_shape.getPen()
    rounded_rect(
        top_pen,
        x1=outer_left, y1=mid_y, x2=outer_right, y2=top,
        radius_v=top_outer_cv, radius_h=top_outer_ch, clockwise=False,
    )
    inner_cv = max(0, top_outer_cv - stroke)
    inner_ch = max(0, top_outer_ch - stroke)
    rounded_rect(
        top_pen,
        x1=outer_left + stroke, y1=mid_y + stroke, x2=outer_right - stroke, y2=top - stroke,
        radius_v=inner_cv, radius_h=inner_ch, clockwise=True,
    )

    # Cut right opening (from mid_y to mid_y + gap)
    gap_top = mid_y + FontConfig.C_GAP_TOP * (top - mid_y)
    cut_right = pathops.Path()
    cr = cut_right.getPen()
    cr.moveTo((FontConfig.WIDTH / 2, mid_y - 1))
    cr.lineTo((FontConfig.WIDTH / 2, gap_top))
    cr.lineTo((FontConfig.WIDTH + 50, gap_top))
    cr.lineTo((FontConfig.WIDTH + 50, mid_y - 1))
    cr.closePath()

    top_result = pathops.op(top_shape, cut_right, pathops.PathOp.DIFFERENCE, fix_winding=True)

    # --- Bottom half: rounded rect from 0 to mid_y, opening on the left ---
    bot_outer_cv = min(v_radius, mid_y / 2)
    bot_outer_ch = min(h_radius, (outer_right - outer_left) / 2)

    bot_shape = pathops.Path()
    bot_pen = bot_shape.getPen()
    rounded_rect(
        bot_pen,
        x1=outer_left, y1=0, x2=outer_right, y2=mid_y,
        radius_v=bot_outer_cv, radius_h=bot_outer_ch, clockwise=False,
    )
    rounded_rect(
        bot_pen,
        x1=outer_left + stroke, y1=stroke, x2=outer_right - stroke, y2=mid_y - stroke,
        radius_v=inner_cv, radius_h=inner_ch, clockwise=True,
    )

    # Cut left opening (from gap to mid_y)
    gap_bottom = mid_y - FontConfig.C_GAP_TOP * mid_y
    cut_left = pathops.Path()
    cl = cut_left.getPen()
    cl.moveTo((-50, gap_bottom))
    cl.lineTo((-50, mid_y + 1))
    cl.lineTo((FontConfig.WIDTH / 2, mid_y + 1))
    cl.lineTo((FontConfig.WIDTH / 2, gap_bottom))
    cl.closePath()

    bot_result = pathops.op(bot_shape, cut_left, pathops.PathOp.DIFFERENCE, fix_winding=True)

    # Union both halves
    result = pathops.op(top_result, bot_result, pathops.PathOp.UNION, fix_winding=True)

    result.draw(pen)
