"""Generate font."""

import importlib
import inspect
import math
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
    SingleSubst,
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


def skew_path(path, angle_deg):
    """Apply an italic skew (horizontal shear) to a pathops.Path."""
    skew = math.tan(math.radians(angle_deg))
    skewed = pathops.Path()
    pen = pathops.PathPen(skewed)
    for verb, points in path:
        transformed = tuple((x + y * skew, y) for x, y in points)
        if verb == pathops.PathVerb.MOVE:
            pen.moveTo(*transformed)
        elif verb == pathops.PathVerb.LINE:
            pen.lineTo(*transformed)
        elif verb == pathops.PathVerb.CUBIC:
            pen.curveTo(*transformed)
        elif verb == pathops.PathVerb.CLOSE:
            pen.closePath()
    return skewed


def select_italic_glyphs(all_glyphs):
    """For each unicode, prefer the glyph with default_italic=True.

    Returns (active_glyphs, italic_promoted_names) where italic_promoted_names
    contains glyph names that were promoted to default for the italic variant
    and should NOT be treated as alternates.
    """
    by_unicode = {}
    for g in all_glyphs:
        if not g.unicode:
            continue
        code = int(g.unicode, 16)
        existing = by_unicode.get(code)
        if existing is None:
            by_unicode[code] = g
        elif g.default_italic and not existing.default_italic:
            by_unicode[code] = g
        elif g.default_italic and existing.default_italic:
            by_unicode[code] = g  # last one wins

    # Names promoted as the italic default (they go into cmap, not alternates)
    promoted = {g.name for g in by_unicode.values()}

    # Build the final list: selected base glyphs + non-unicode glyphs (ligatures etc.)
    result = list(by_unicode.values())
    for g in all_glyphs:
        if not g.unicode and g.name not in promoted:
            result.append(g)
    return result, promoted


def build_gsub(glyph_names, ligature_glyphs, alternate_glyphs, cmap):
    """Build a GSUB table with ligature and alternate substitutions."""
    gsub_table = newTable("GSUB")
    gsub = GSUB()
    gsub.Version = 0x00010000
    gsub_table.table = gsub

    lookups = []
    feature_records = []

    # Reverse cmap: unicode int -> base glyph name
    base_by_unicode = {unicode_val: name for unicode_val, name in cmap.items()}

    # Build alternate substitution lookups grouped by feature tag
    feature_lookups = {}
    for g in alternate_glyphs:
        if g.name not in glyph_names or not g.unicode:
            continue
        base_name = base_by_unicode.get(int(g.unicode, 16))
        if not base_name:
            continue
        for tag in g.font_feature:
            feature_lookups.setdefault(tag, {})
            feature_lookups[tag][base_name] = g.name

    for tag in sorted(feature_lookups):
        subst = SingleSubst()
        subst.mapping = feature_lookups[tag]

        lookup = Lookup()
        lookup.LookupType = 1  # Single substitution
        lookup.LookupFlag = 0
        lookup.SubTableCount = 1
        lookup.SubTable = [subst]

        lookup_idx = len(lookups)
        lookups.append(lookup)

        feature = Feature()
        feature.FeatureParams = None
        feature.LookupListIndex = [lookup_idx]
        feature.LookupCount = 1

        feat_record = FeatureRecord()
        feat_record.FeatureTag = tag
        feat_record.Feature = feature
        feature_records.append(feat_record)

    # Build ligature substitution lookup
    if ligature_glyphs:
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

        lookup_idx = len(lookups)
        lookups.append(lookup)

        feature = Feature()
        feature.FeatureParams = None
        feature.LookupListIndex = [lookup_idx]
        feature.LookupCount = 1

        feat_record = FeatureRecord()
        feat_record.FeatureTag = "liga"
        feat_record.Feature = feature
        feature_records.append(feat_record)

    gsub.LookupList = LookupList()
    gsub.LookupList.LookupCount = len(lookups)
    gsub.LookupList.Lookup = lookups

    gsub.FeatureList = FeatureList()
    gsub.FeatureList.FeatureCount = len(feature_records)
    gsub.FeatureList.FeatureRecord = feature_records

    # Script: DFLT with default lang sys referencing all features
    lang_sys = DefaultLangSys()
    lang_sys.ReqFeatureIndex = 0xFFFF
    lang_sys.FeatureIndex = list(range(len(feature_records)))
    lang_sys.FeatureCount = len(feature_records)

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


def build_font(output_path=None, bold=False, italic=False):
    if bold and italic:
        style_name = "BoldItalic"
    elif bold:
        style_name = "Bold"
    elif italic:
        style_name = "Italic"
    else:
        style_name = "Regular"

    if output_path is None:
        output_path = f"fonts/{fc.family_name}-{style_name}.otf"

    dc = DrawConfig.bold() if bold else DrawConfig()

    all_glyphs = discover_glyphs()

    # For italic, prefer glyphs with default_italic=True
    if italic:
        active_glyphs, promoted = select_italic_glyphs(all_glyphs)
    else:
        active_glyphs = all_glyphs
        promoted = set()

    cmap = {0x20: "space"}
    ligature_glyphs = []
    alternate_glyphs = []
    for g in active_glyphs:
        if g.font_feature and g.name not in promoted:
            alternate_glyphs.append(g)
        elif g.unicode:
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
    for g in active_glyphs:
        path = simplify_glyph(g, dc=dc)
        if italic:
            path = skew_path(path, fc.italic_angle)
        pen = T2CharStringPen(fc.window_width, None)
        path.draw(pen)
        charstrings[g.name] = pen.getCharString()

    glyph_names = list(charstrings.keys())

    fb = FontBuilder(fc.units_per_em, isTTF=False)
    fb.setupGlyphOrder(glyph_names)
    fb.setupCharacterMap(cmap)
    # Alignment zones for CFF hinting
    # BlueValues: pairs of [flat_edge, overshoot_edge] for zones at or above baseline
    # OtherBlues: pairs for zones below baseline (descender)
    ov = fc.v_overshoot
    blue_values = [
        -ov, 0,                       # baseline (overshoot below)
        fc.x_height, fc.x_height + ov, # x-height
        fc.cap, fc.cap + ov,           # cap height
        fc.ascent, fc.ascent + ov,     # ascender
    ]
    other_blues = [
        fc.descent - ov, fc.descent,   # descender
    ]

    fb.setupCFF(
        psName=f"{fc.family_name}-{style_name}",
        fontInfo={"FullName": f"{fc.family_name} {style_name}"},
        charStringsDict=charstrings,
        privateDict={
            "BlueValues": blue_values,
            "OtherBlues": other_blues,
            "BlueShift": 7,
            "BlueFuzz": 1,
        },
    )
    # Ligature glyphs get wider advance width based on number_characters
    glyph_by_name = {g.name: g for g in active_glyphs}
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

    # fsSelection / macStyle flags
    fs_selection = 0x0000
    mac_style = 0x0000
    if bold:
        fs_selection |= 0x0020  # BOLD
        mac_style |= 0x0001
    if italic:
        fs_selection |= 0x0001  # ITALIC
        mac_style |= 0x0002
    if not bold and not italic:
        fs_selection |= 0x0040  # REGULAR

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
    ital_angle = -fc.italic_angle if italic else 0
    fb.setupPost(isFixedPitch=1, italicAngle=ital_angle)
    fb.setupHead(unitsPerEm=fc.units_per_em, macStyle=mac_style)

    # GSUB table for ligatures and alternates
    if ligature_glyphs or alternate_glyphs:
        fb.font["GSUB"] = build_gsub(glyph_names, ligature_glyphs, alternate_glyphs, cmap)

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
    build_ttf(ttf_path, style_name, active_glyphs, cmap, dc, ligature_glyphs, alternate_glyphs, italic)


def build_ttf(output_path, style_name, all_glyphs, cmap, dc, ligature_glyphs, alternate_glyphs, italic=False):
    """Build a TTF font with quadratic outlines from scratch."""
    from fontTools.pens.cu2quPen import Cu2QuPen
    from fontTools.pens.ttGlyphPen import TTGlyphPen

    def record_ttf_glyph(glyph):
        path = simplify_glyph(glyph, dc=dc)
        if italic:
            path = skew_path(path, fc.italic_angle)
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

    bold = "Bold" in style_name
    fs_selection = 0x0000
    mac_style = 0x0000
    if bold:
        fs_selection |= 0x0020
        mac_style |= 0x0001
    if italic:
        fs_selection |= 0x0001
        mac_style |= 0x0002
    if not bold and not italic:
        fs_selection |= 0x0040

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
    ital_angle = -fc.italic_angle if italic else 0
    fb.setupPost(isFixedPitch=1, italicAngle=ital_angle)
    fb.setupHead(unitsPerEm=fc.units_per_em, macStyle=mac_style)

    # GSUB table for ligatures and alternates
    if ligature_glyphs or alternate_glyphs:
        fb.font["GSUB"] = build_gsub(glyph_names, ligature_glyphs, alternate_glyphs, cmap)

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
    build_font(italic=True)
    build_font(bold=True, italic=True)
