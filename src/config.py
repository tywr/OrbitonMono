from dataclasses import dataclass
from utils.bounds import BodyBounds


@dataclass
class FontConfig:
    family_name: str = "Kassiopea"

    units_per_em: int = 1000
    window_ascent: int = 1025
    window_descent: int = -300
    window_width: int = 580

    ascent: int = 775
    descent: int = -200
    cap: int = 725
    x_height: int = 520

    accent: int = 710
    accent_cap: int = 890

    math: int = 345

    parenthesis: int = 345
    parenthesis_length: int = 920

    default_stroke = 90
    italic_angle: float = 9.4

    v_overshoot: int = 10
    h_overshoot: int = 10


@dataclass
class DrawConfig(FontConfig):
    # Default parameters
    stroke_x: int = 86
    stroke_y: int = 78
    stroke_alt: int = 66
    width: int = 348

    hx: int = 172
    hy: int = 200

    cap_hx: int = 182
    cap_hy: int = 208

    gap: int = 10

    number_hx: int = 160
    number_hy: int = 240

    # Taper values
    taper: float = 0.4
    taper_a: float = 0.15
    taper_r: float = 0.15

    @classmethod
    def bold(cls):
        """Return a DrawConfig with heavier stroke weights for a bold variant."""
        ratio = 1.24
        return cls(
            stroke_x=int(cls.stroke_x * ratio),
            stroke_y=int(cls.stroke_y * ratio),
            stroke_alt=int(cls.stroke_alt * ratio),
            taper=cls.taper,
        )

    @classmethod
    def italic(cls):
        ratio_y = 0.92
        ratio_alt = 0.92
        return cls(
            stroke_x=int(cls.stroke_x),
            stroke_y=int(cls.stroke_y * ratio_y),
            stroke_alt=int(cls.stroke_alt * ratio_alt),
            taper=cls.taper,
            gap=0,
        )

    def body_bounds(
        self,
        offset: int,
        width_ratio=1,
        height="x_height",
        overshoot_left=False,
        overshoot_right=False,
        overshoot_top=False,
        overshoot_bottom=False,
        number=False,
        uppercase=False,
    ):
        """
        Abstraction for storing common metrics relative to the body
        of a character. For most lowercase, the boundaries are
        a centered rectangle of length `width` and of height `x-height`.
        For most capital letters, it's a centered rectangle of length
        `width` of a of height `ascent`.
        """
        width = self.width * width_ratio
        if height not in ["x_height", "ascent", "cap"]:
            raise ValueError(f"Value {height} should be `x_height`, `ascent` or `cap`")
        x1 = self.window_width / 2 - width / 2 - self.stroke_x / 2 + offset
        y1 = 0
        x2 = self.window_width / 2 + width / 2 + self.stroke_x / 2 + offset
        y2 = getattr(self, height)

        if overshoot_left:
            x1 -= self.h_overshoot
        if overshoot_right:
            x2 += self.h_overshoot

        if overshoot_bottom:
            y1 -= self.v_overshoot
        if overshoot_top:
            y2 += self.v_overshoot

        # Rescale the hx and hy for the new box
        if number:
            hx = self.number_hx
            hy = self.number_hy
        elif uppercase:
            hx = self.cap_hx
            hy = self.cap_hy
        else:
            hx = self.hx
            hy = self.hy

        hx = hx * (x2 - x1 - self.stroke_x) / self.width
        hy = hy * (y2 - y1 - self.stroke_y) / self.x_height

        return BodyBounds(x1=x1, y1=y1, x2=x2, y2=y2, hx=hx, hy=hy)
