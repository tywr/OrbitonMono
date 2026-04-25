from dataclasses import dataclass
from utils.bounds import BodyBounds


@dataclass
class FontConfig:
    family_name: str = "Kassiopea"

    units_per_em: int = 1000
    window_ascent: int = 1025
    window_descent: int = -300
    window_width: int = 580

    ascent: int = 750
    descent: int = -200
    cap: int = 710
    x_height: int = 520

    accent: int = 685
    accent_cap: int = 890

    math: int = 300

    parenthesis: int = 300
    parenthesis_length: int = 1060

    min_margin: int = 25

    default_stroke = 90
    italic_angle: float = 9.4


@dataclass
class DrawConfig(FontConfig):
    # Can be overwritten for bold / thinner fonts
    x_height: int = FontConfig.x_height
    cap: int = FontConfig.cap
    ascent: int = FontConfig.ascent
    descent: int = FontConfig.descent
    accent: int = FontConfig.accent
    accent_cap: int = FontConfig.accent_cap

    # Default parameters
    stroke_x: int = 94
    stroke_y: int = 66
    stroke_alt: int = 62

    v_overshoot: int = 12
    h_overshoot: int = 11

    width: int = 366

    hx: int = 172
    hy: int = 164

    cap_hx: int = 186
    cap_hy: int = 178

    gap: int = 10

    taper: float = 0.5

    italic: bool = False

    @classmethod
    def weight(cls, w=400):
        """Return a DrawConfig with heavier stroke weights for a bold variant."""
        from math import log, exp

        brx = 1.5
        ratio_x = exp((w - 400) * log(brx) / 300)

        bry = 1.25
        ratio_y = exp((w - 400) * log(bry) / 300)

        bhy = 1.3
        hy_ratio = exp((w - 400) * log(bhy) / 300)

        # Function mapping 100 → 0.5 and 700 → 0.2
        taper = min(0.5, 0.5 - 0.0007 * (w - 400))

        extra_height = int((ratio_y - 1) * cls.stroke_y)
        return cls(
            stroke_x=int(cls.stroke_x * ratio_x),
            stroke_y=int(cls.stroke_y * ratio_y),
            stroke_alt=int(cls.stroke_alt * ratio_y),
            x_height=cls.x_height + extra_height,
            cap=cls.cap + extra_height,
            accent=cls.cap + extra_height,
            accent_cap=cls.accent_cap + extra_height,
            ascent=cls.ascent + extra_height,
            descent=cls.descent - extra_height,
            taper=taper,
            hy=hy_ratio * cls.hy,
            cap_hy=hy_ratio * cls.cap_hy,
        )

    @classmethod
    def for_italic(cls):
        return cls(
            stroke_x=int(cls.stroke_x),
            stroke_y=int(cls.stroke_y),
            stroke_alt=int(cls.stroke_alt),
            taper=cls.taper,
            gap=0,
            italic=True,
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
        min_margin=None,
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

        # For some wide characters (w, m, W, M) we fix a min margin for bolder
        # weights
        if min_margin:
            x1 = max(min_margin, x1)
            x2 = min(self.window_width - min_margin, x2)

        v_ov = self.v_overshoot
        h_ov = self.h_overshoot
        # if uppercase:
        #     v_ov *= 0.6 * self.cap / self.x_height

        if overshoot_left:
            x1 -= h_ov / 2
            x2 += h_ov / 2
        if overshoot_right:
            x1 -= h_ov / 2
            x2 += h_ov / 2

        if overshoot_bottom:
            y1 -= v_ov
        if overshoot_top:
            y2 += v_ov

        # Rescale the hx and hy for the new box
        if uppercase:
            hx = self.cap_hx
            hy = self.cap_hy
        else:
            hx = self.hx
            hy = self.hy

        hx = hx * (x2 - x1 - self.stroke_x) / self.width
        hy = hy * (y2 - y1 - self.stroke_y) / self.x_height

        return BodyBounds(
            x1=x1, y1=y1, x2=x2, y2=y2, hx=hx, hy=hy, v_ov=v_ov, h_ov=h_ov
        )
