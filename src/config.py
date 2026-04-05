from dataclasses import dataclass
from utils.bounds import BodyBounds


@dataclass
class FontConfig:
    family_name: str = "Kassiopea"

    units_per_em: int = 1000
    window_ascent: int = 1020
    window_descent: int = -300
    window_width: int = 600

    ascent: int = 730
    descent: int = -200
    cap: int = 730
    x_height: int = 550
    accent: int = 710

    default_stroke = 90


@dataclass
class DrawConfig(FontConfig):
    # Default parameters
    stroke_x: int = 90
    stroke_y: int = 70
    width: int = 340
    hx: int = 200
    hy: int = 200
    taper: float = 0.25
    # hx: int = 180
    # hy: int = 180
    # taper: float = 0.4
    gap: int = 5
    v_overshoot: int = 10
    h_overshoot: int = 5

    def body_bounds(
        self,
        offset: int,
        overshoot_left=False,
        overshoot_right=False,
        overshoot_top=False,
        overshoot_bottom=False,
        height="x_height",
        width_ratio=1,
    ):
        """
        Abstraction for storing common metrics relative to the body
        of a character. For most lowercase, the boundaries are
        a centered rectangle of length `width` and of height `x-height`.
        For most capital letters, it's a centered rectangle of length
        `width` of a of height `ascent`.
        """
        width = self.width * width_ratio
        if height not in ["x_height", "ascent"]:
            raise ValueError(f"Value {height} should be `x_height` or `ascent`")
        x1 = self.window_width / 2 - width / 2 - self.stroke_x / 2 + offset
        y1 = 0
        x2 = self.window_width / 2 + width / 2 + self.stroke_x / 2 + offset
        y2 = getattr(self, height)

        # Add horizontal overshoots
        if overshoot_left:
            x1 -= self.h_overshoot
        if overshoot_right:
            x2 += self.h_overshoot

        if overshoot_bottom:
            y1 -= self.v_overshoot
        if overshoot_top:
            y2 += self.v_overshoot

        return BodyBounds(x1=x1, y1=y1, x2=x2, y2=y2)
