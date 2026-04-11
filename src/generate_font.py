"""Generate font."""

import importlib
import inspect
import pkgutil

import pathops
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen

from fontTools.ttLib.tables.otTables import (
    GSUB,
    DefaultLangSys,
    Feature,
    FeatureList,
    FeatureRecord,
    Ligature,
    LigatureSubst,
    Lookup,
    LookupList,
    Script,
    ScriptList,
    ScriptRecord,
)
from fontTools.ttLib import newTable

from config import FontConfig as fc
from config import DrawConfig
from glyphs import Glyph, LigatureGlyph

import glyphs


def discover_glyphs():
    """Recursively import all modules under glyphs/ and return Glyph subclasses."""

    def on_error(name):
        raise ImportError(f"Failed to import {name}")

    for pkg in [glyphs]:
        for importer, modname, ispkg in pkgutil.walk_packages(
            pkg.__path__, pkg.__name__ + ".", onerror=on_error
        ):
            importlib.import_module(modname)

    def all_subclasses(cls):
        result = []
        for sub in cls.__subclasses__():
            if not inspect.isabstract(sub):
                result.append(sub)
            result.extend(all_subclasses(sub))
        return result

    return [cls() for cls in all_subclasses(Glyph)]


def draw_notdef(pen):
    pen.moveTo((50, 0))
    pen.lineTo((50, 700))
    pen.lineTo((450, 700))
    pen.lineTo((450, 0))
    pen.closePath()


def simplify_glyph(glyph, **kwargs):
    """Draw a glyph through pathops and return the simplified pathops.Path."""
    path = pathops.Path()
    glyph.draw(pathops.PathPen(path), **kwargs)
    return pathops.simplify(path, clockwise=False, keep_starting_points=True)


def record_glyph(glyph, **kwargs):
    path = simplify_glyph(glyph, **kwargs)
    pen = T2CharStringPen(fc.window_width, None)
    path.draw(pen)
    return pen.getCharString()


def build_gsub(glyph_names, ligature_glyphs):
    """Build a GSUB table with ligature substitutions."""
    gsub_table = newTable("GSUB")
    gsub = GSUB()
    gsub.Version = 0x00010000
    gsub_table.table = gsub

    # Build ligature subtable grouped by first component
    lig_by_first = {}
    for g in ligature_glyphs:
        if g.name not in glyph_names:
            continue
        first = g.components[0]
        rest = g.components[1:]
        lig = Ligature()
        lig.LigGlyph = g.name
        lig.Component = rest
        lig.CompCount = len(g.components)
        lig_by_first.setdefault(first, []).append(lig)

    subst = LigatureSubst()
    subst.ligatures = lig_by_first

    lookup = Lookup()
    lookup.LookupType = 4  # Ligature substitution
    lookup.LookupFlag = 0
    lookup.SubTableCount = 1
    lookup.SubTable = [subst]

    gsub.LookupList = LookupList()
    gsub.LookupList.LookupCount = 1
    gsub.LookupList.Lookup = [lookup]

    # Feature: 'liga' (standard ligatures)
    feature = Feature()
    feature.FeatureParams = None
    feature.LookupListIndex = [0]
    feature.LookupCount = 1

    feat_record = FeatureRecord()
    feat_record.FeatureTag = "liga"
    feat_record.Feature = feature

    gsub.FeatureList = FeatureList()
    gsub.FeatureList.FeatureCount = 1
    gsub.FeatureList.FeatureRecord = [feat_record]

    # Script: DFLT with default lang sys
    lang_sys = DefaultLangSys()
    lang_sys.ReqFeatureIndex = 0xFFFF
    lang_sys.FeatureIndex = [0]
    lang_sys.FeatureCount = 1

    script = Script()
    script.DefaultLangSys = lang_sys
    script.LangSysRecord = []
    script.LangSysCount = 0

    script_record = ScriptRecord()
    script_record.ScriptTag = "DFLT"
    script_record.Script = script

    gsub.ScriptList = ScriptList()
    gsub.ScriptList.ScriptCount = 1
    gsub.ScriptList.ScriptRecord = [script_record]

    return gsub_table


def build_font(output_path=None, bold=False):
    style_name = "Bold" if bold else "Regular"
    if output_path is None:
        output_path = f"fonts/{fc.family_name}-{style_name}.otf"

    dc = DrawConfig.bold() if bold else DrawConfig()

    all_glyphs = discover_glyphs()

    cmap = {0x20: "space"}
    ligature_glyphs = []
    for g in all_glyphs:
        if g.unicode:
            cmap[int(g.unicode, 16)] = g.name
        if isinstance(g, LigatureGlyph):
            ligature_glyphs.append(g)

    # Build charstrings
    notdef_pen = T2CharStringPen(fc.window_width, None)
    draw_notdef(notdef_pen)

    space_pen = T2CharStringPen(fc.window_width, None)

    charstrings = {
        ".notdef": notdef_pen.getCharString(),
        "space": space_pen.getCharString(),
    }
    for g in all_glyphs:
        charstrings[g.name] = record_glyph(g, dc=dc)

    glyph_names = list(charstrings.keys())

    fb = FontBuilder(fc.units_per_em, isTTF=False)
    fb.setupGlyphOrder(glyph_names)
    fb.setupCharacterMap(cmap)
    fb.setupCFF(
        psName=f"{fc.family_name}-{style_name}",
        fontInfo={"FullName": f"{fc.family_name} {style_name}"},
        charStringsDict=charstrings,
        privateDict={},
    )
    # Ligature glyphs get wider advance width based on number_characters
    glyph_by_name = {g.name: g for g in all_glyphs}
    metrics = {}
    for name in glyph_names:
        g = glyph_by_name.get(name)
        n = g.number_characters if g else 1
        metrics[name] = (fc.window_width * n, 0)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=fc.window_ascent, descent=-abs(fc.window_descent))
    fb.setupNameTable(
        {
            "familyName": fc.family_name,
            "styleName": style_name,
            "uniqueFontIdentifier": f"{fc.family_name}-{style_name}",
            "fullName": f"{fc.family_name} {style_name}",
            "version": "Version 1.000",
            "psName": f"{fc.family_name}-{style_name}",
        }
    )

    # fsSelection / macStyle flags for bold
    fs_selection = 0x0020 if bold else 0x0040  # BOLD or REGULAR
    mac_style = 0x0001 if bold else 0x0000

    fb.setupOS2(
        sTypoAscender=fc.ascent,
        sTypoDescender=fc.descent,
        sTypoLineGap=50,
        usWinAscent=fc.window_ascent,
        usWinDescent=abs(fc.window_descent),
        sxHeight=fc.x_height,
        sCapHeight=fc.cap,
        fsType=0,
        fsSelection=fs_selection,
    )
    fb.setupPost(isFixedPitch=1)
    fb.setupHead(unitsPerEm=fc.units_per_em, macStyle=mac_style)

    # GSUB table for ligatures
    if ligature_glyphs:
        fb.font["GSUB"] = build_gsub(glyph_names, ligature_glyphs)

    # Dummy DSIG so macOS validators don't complain
    dsig = newTable("DSIG")
    dsig.ulVersion = 1
    dsig.usFlag = 0
    dsig.usNumSigs = 0
    dsig.signatureRecords = []
    fb.font["DSIG"] = dsig

    fb.font.save(output_path)
    print(f"Font saved to {output_path}")

    # Build TTF version
    ttf_path = output_path.replace(".otf", ".ttf")
    build_ttf(ttf_path, style_name, all_glyphs, cmap, dc, ligature_glyphs)


def build_ttf(output_path, style_name, all_glyphs, cmap, dc, ligature_glyphs):
    """Build a TTF font with quadratic outlines from scratch."""
    from fontTools.pens.cu2quPen import Cu2QuPen
    from fontTools.pens.ttGlyphPen import TTGlyphPen

    def record_ttf_glyph(glyph):
        path = simplify_glyph(glyph, dc=dc)
        ttf_pen = TTGlyphPen(None)
        cu2qu_pen = Cu2QuPen(ttf_pen, max_err=1.0, reverse_direction=False)
        path.draw(cu2qu_pen)
        return ttf_pen.glyph()

    # .notdef
    notdef_pen = TTGlyphPen(None)
    draw_notdef(notdef_pen)

    # space (empty)
    space_pen = TTGlyphPen(None)
    space_pen.glyph()  # finalize empty glyph

    glyph_table = {".notdef": notdef_pen.glyph(), "space": TTGlyphPen(None).glyph()}
    for g in all_glyphs:
        glyph_table[g.name] = record_ttf_glyph(g)

    glyph_names = list(glyph_table.keys())

    fb = FontBuilder(fc.units_per_em, isTTF=True)
    fb.setupGlyphOrder(glyph_names)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyph_table)
    # LSB must match glyf xMin for correct TTF rendering
    glyph_by_name = {g.name: g for g in all_glyphs}
    metrics = {}
    for name in glyph_names:
        ttf_g = glyph_table[name]
        lsb = ttf_g.xMin if hasattr(ttf_g, "xMin") and ttf_g.numberOfContours > 0 else 0
        src_g = glyph_by_name.get(name)
        n = src_g.number_characters if src_g else 1
        metrics[name] = (fc.window_width * n, lsb)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=fc.window_ascent, descent=-abs(fc.window_descent))
    fb.setupNameTable(
        {
            "familyName": fc.family_name,
            "styleName": style_name,
            "uniqueFontIdentifier": f"{fc.family_name}-{style_name}",
            "fullName": f"{fc.family_name} {style_name}",
            "version": "Version 1.000",
            "psName": f"{fc.family_name}-{style_name}",
        }
    )

    fs_selection = 0x0020 if style_name == "Bold" else 0x0040
    mac_style = 0x0001 if style_name == "Bold" else 0x0000

    fb.setupOS2(
        sTypoAscender=fc.ascent,
        sTypoDescender=fc.descent,
        sTypoLineGap=50,
        usWinAscent=fc.window_ascent,
        usWinDescent=abs(fc.window_descent),
        sxHeight=fc.x_height,
        sCapHeight=fc.cap,
        fsType=0,
        fsSelection=fs_selection,
    )
    fb.setupPost(isFixedPitch=1)
    fb.setupHead(unitsPerEm=fc.units_per_em, macStyle=mac_style)

    # GSUB table for ligatures
    if ligature_glyphs:
        fb.font["GSUB"] = build_gsub(glyph_names, ligature_glyphs)

    dsig = newTable("DSIG")
    dsig.ulVersion = 1
    dsig.usFlag = 0
    dsig.usNumSigs = 0
    dsig.signatureRecords = []
    fb.font["DSIG"] = dsig

    fb.font.save(output_path)
    print(f"Font saved to {output_path}")


if __name__ == "__main__":
    build_font(bold=False)
    build_font(bold=True)
