"""Generate a minimal TTF font containing the letter 'o'."""

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

from config import FontConfig
from characters.o import draw_o
from characters.c import draw_c
from characters.b import draw_b
from characters.d import draw_d
from characters.g import draw_g
from characters.p import draw_p
from characters.h import draw_h
from characters.m import draw_m
from characters.n import draw_n
from characters.q import draw_q
from characters.r import draw_r
from characters.u import draw_u
from characters.y import draw_y


def draw_notdef(pen):
    """Simple rectangle for the .notdef glyph."""
    pen.moveTo((50, 0))
    pen.lineTo((50, 700))
    pen.lineTo((450, 700))
    pen.lineTo((450, 0))
    pen.closePath()


def build_font(output_path="OrbitonMono.ttf"):
    fb = FontBuilder(FontConfig.UNITS_PER_EM, isTTF=True)
    fb.setupGlyphOrder([".notdef", "space", "o", "c", "b", "d", "g", "h", "m", "n", "p", "q", "r", "u", "y"])
    fb.setupCharacterMap({
        32: "space", 111: "o", 99: "c",
        98: "b", 100: "d", 103: "g", 104: "h", 109: "m", 110: "n", 112: "p", 113: "q",
        114: "r", 117: "u", 121: "y",
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

    g_pen = TTGlyphPen(None)
    draw_g(g_pen, font_config=FontConfig, stroke=60)

    p_pen = TTGlyphPen(None)
    draw_p(p_pen, font_config=FontConfig, stroke=60)

    h_pen = TTGlyphPen(None)
    draw_h(h_pen, font_config=FontConfig, stroke=60)

    m_pen = TTGlyphPen(None)
    draw_m(m_pen, font_config=FontConfig, stroke=60)

    n_pen = TTGlyphPen(None)
    draw_n(n_pen, font_config=FontConfig, stroke=60)

    q_pen = TTGlyphPen(None)
    draw_q(q_pen, font_config=FontConfig, stroke=60)

    r_pen = TTGlyphPen(None)
    draw_r(r_pen, font_config=FontConfig, stroke=60)

    u_pen = TTGlyphPen(None)
    draw_u(u_pen, font_config=FontConfig, stroke=60)

    y_pen = TTGlyphPen(None)
    draw_y(y_pen, font_config=FontConfig, stroke=60)

    fb.setupGlyf(
        {
            ".notdef": notdef_pen.glyph(),
            "space": space_pen.glyph(),
            "o": o_pen.glyph(),
            "c": c_pen.glyph(),
            "b": b_pen.glyph(),
            "d": d_pen.glyph(),
            "g": g_pen.glyph(),
            "h": h_pen.glyph(),
            "m": m_pen.glyph(),
            "n": n_pen.glyph(),
            "p": p_pen.glyph(),
            "q": q_pen.glyph(),
            "r": r_pen.glyph(),
            "u": u_pen.glyph(),
            "y": y_pen.glyph(),
        }
    )

    # Compute LSB from actual glyph bounds so renderers don't shift glyphs
    glyf_table = fb.font["glyf"]
    metrics = {}
    for name in fb.font.getGlyphOrder():
        glyph = glyf_table[name]
        if glyph.numberOfContours == 0 or not hasattr(glyph, "xMin"):
            lsb = 0
        else:
            lsb = glyph.xMin
        metrics[name] = (FontConfig.WIDTH, lsb)
    fb.setupHorizontalMetrics(metrics)

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
