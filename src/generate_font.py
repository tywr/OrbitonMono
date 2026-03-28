"""Generate a minimal TTF font containing the letter 'o'."""

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

from config import FontConfig
from characters.o import draw_o
from characters.c import draw_c
from characters.b import draw_b
from characters.d import draw_d
from characters.p import draw_p
from characters.n import draw_n
from characters.q import draw_q


def draw_notdef(pen):
    """Simple rectangle for the .notdef glyph."""
    pen.moveTo((50, 0))
    pen.lineTo((50, 700))
    pen.lineTo((450, 700))
    pen.lineTo((450, 0))
    pen.closePath()


def build_font(output_path="OrbitonMono.ttf"):
    fb = FontBuilder(FontConfig.UNITS_PER_EM, isTTF=True)
    fb.setupGlyphOrder([".notdef", "space", "o", "c", "b", "d", "n", "p", "q"])
    fb.setupCharacterMap({
        32: "space", 111: "o", 99: "c",
        98: "b", 100: "d", 110: "n", 112: "p", 113: "q",
    })

    notdef_pen = TTGlyphPen(None)
    draw_notdef(notdef_pen)

    space_pen = TTGlyphPen(None)

    o_pen = TTGlyphPen(None)
    draw_o(o_pen, font_config=FontConfig, stroke=60)

    c_pen = TTGlyphPen(None)
    draw_c(c_pen, font_config=FontConfig, stroke=60)

    b_pen = TTGlyphPen(None)
    draw_b(b_pen, font_config=FontConfig, stroke=60)

    d_pen = TTGlyphPen(None)
    draw_d(d_pen, font_config=FontConfig, stroke=60)

    p_pen = TTGlyphPen(None)
    draw_p(p_pen, font_config=FontConfig, stroke=60)

    n_pen = TTGlyphPen(None)
    draw_n(n_pen, font_config=FontConfig, stroke=60)

    q_pen = TTGlyphPen(None)
    draw_q(q_pen, font_config=FontConfig, stroke=60)

    fb.setupGlyf(
        {
            ".notdef": notdef_pen.glyph(),
            "space": space_pen.glyph(),
            "o": o_pen.glyph(),
            "c": c_pen.glyph(),
            "b": b_pen.glyph(),
            "d": d_pen.glyph(),
            "n": n_pen.glyph(),
            "p": p_pen.glyph(),
            "q": q_pen.glyph(),
        }
    )

    fb.setupHorizontalMetrics(
        {
            ".notdef": (500, 50),
            "space": (500, 0),
            "o": (500, 20),
            "c": (500, 20),
            "b": (500, 20),
            "d": (500, 20),
            "n": (500, 20),
            "p": (500, 20),
            "q": (500, 20),
        }
    )

    fb.setupHorizontalHeader(ascent=FontConfig.ASCENT, descent=FontConfig.DESCENT)
    fb.setupNameTable(
        {
            "familyName": FontConfig.FAMILY_NAME,
            "styleName": "Regular",
        }
    )
    fb.setupOS2(sTypoAscender=FontConfig.ASCENT, sTypoDescender=FontConfig.DESCENT, sTypoLineGap=0)
    fb.setupPost()

    fb.font.save(output_path)
    print(f"Font saved to {output_path}")


if __name__ == "__main__":
    build_font()
