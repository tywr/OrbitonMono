#!/usr/bin/env python3
"""Render syntax-highlighted code snippets as PNGs using Nordwand Mono.

Usage: python -m scripts.samples
"""

import argparse
import os

from PIL import Image, ImageDraw, ImageFont
from pygments import highlight
from pygments.filters import TokenMergeFilter
from pygments.formatters import ImageFormatter
from pygments.lexers import (
    CppLexer,
    HaskellLexer,
    MarkdownLexer,
    PythonLexer,
    TextLexer,
)
from pygments.style import Style
from pygments.token import (
    Comment,
    Error,
    Generic,
    Keyword,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Text,
)


# Pygments' ImageFormatter calls PIL's draw.text() without OpenType features,
# so ligatures/calt never fire. Inject them globally — Pillow needs libraqm,
# which we've checked is present.
_orig_pil_text = ImageDraw.ImageDraw.text


def _pil_text_with_features(self, *args, **kwargs):
    kwargs.setdefault("features", ["liga", "calt"])
    return _orig_pil_text(self, *args, **kwargs)


ImageDraw.ImageDraw.text = _pil_text_with_features


# Gravity palette (~/.config/colorthemes/monochrome/gravity.yaml)
BG = "#121212"
FG = "#cccccc"
FG_BRIGHT = "#eeeeee"
PRIMARY = "#91c7d9"
PRIMARY_BRIGHT = "#abeaff"
CONTRAST = "#af875f"
CONTRAST_BRIGHT = "#d7af87"

# 10-step monochrome gradient from foreground (noir_0) toward background (noir_9),
# mirroring the noir_N scale used in ~/.config/nvim/lua/noir.lua.
NOIR_0 = "#cccccc"
NOIR_1 = "#b3b3b3"
NOIR_2 = "#9a9a9a"
NOIR_3 = "#808080"
NOIR_4 = "#707070"
NOIR_5 = "#606060"
NOIR_6 = "#505050"
NOIR_7 = "#424242"
NOIR_8 = "#2c2c2c"
NOIR_9 = "#1f1f1f"


class GravityNoirStyle(Style):
    """Monochrome syntax style mirroring the noir.lua treesitter mapping."""

    background_color = BG
    highlight_color = NOIR_8

    styles = {
        Text: FG,
        Comment: f"italic {NOIR_7}",
        Comment.Preproc: NOIR_2,
        Keyword: NOIR_5,
        Keyword.Constant: PRIMARY,  # True / False / None
        Keyword.Namespace: NOIR_6,  # import / from
        Keyword.Pseudo: NOIR_5,
        Keyword.Reserved: NOIR_5,
        Keyword.Type: NOIR_6,
        Operator: NOIR_6,
        Operator.Word: NOIR_5,  # and / or / not
        Punctuation: NOIR_2,
        Name: NOIR_2,
        Name.Function: f"bold {FG}",
        Name.Function.Magic: f"bold {NOIR_2}",
        Name.Class: NOIR_1,
        Name.Builtin: NOIR_2,
        Name.Builtin.Pseudo: NOIR_2,  # self / cls
        Name.Decorator: f"bold {PRIMARY}",
        Name.Namespace: NOIR_2,
        Name.Variable: NOIR_2,
        Name.Variable.Magic: NOIR_2,  # __name__ / __init__
        Name.Constant: NOIR_2,
        Name.Attribute: NOIR_2,
        Name.Tag: NOIR_6,
        Name.Exception: NOIR_2,
        String: PRIMARY,
        String.Doc: f"italic {PRIMARY}",
        String.Escape: NOIR_2,
        String.Interpol: NOIR_2,
        String.Affix: NOIR_5,  # f / r / b prefix
        Number: PRIMARY,
        Error: PRIMARY,
        Generic.Heading: f"bold {FG_BRIGHT}",
        Generic.Subheading: f"bold {NOIR_1}",
        Generic.Strong: f"bold {FG}",
        Generic.Emph: f"italic {NOIR_2}",
        Generic.Inserted: PRIMARY,
        Generic.Deleted: CONTRAST,
    }


SAMPLE_CHAR = """\
ABCDEFGHIJKLMNOPQRSTUVWXYZ
abcdefghijklmnopqrstuvwxyz
0123456789
!"#$%&'()+=,-./:;<*>
?@[\]^_`{|}~
-> => __ -- == ===
"""


SAMPLE_1 = '''\
def fibonacci(n: int) -> list[int]:
    """Return the first n Fibonacci numbers."""
    seq = [0, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq[:n]


if __name__ == "__main__":
    print(fibonacci(10))
'''


SAMPLE_2 = """\
#include <vector>
#include <iostream>

template <typename T>
auto max_element(const std::vector<T>& xs) -> T {
    T best = xs[0];
    for (const auto& x : xs) {
        if (x >= best) best = x;
    }
    return best;
}

int main() {
    std::vector<int> v {3, 1, 4, 1, 5, 9, 2, 6};
    std::cout << "max = " << max_element(v) << "\\n";
    return 0;
}
"""


SAMPLE_3 = """\
module Fib where

import Data.List (foldl\\')

-- | Infinite list of Fibonacci numbers.
fibs :: [Integer]
fibs = 0 : 1 : zipWith (+) fibs (tail fibs)

fact :: Int -> Integer
fact n = foldl\\' (*) 1 [1..fromIntegral n]

main :: IO ()
main = do
  let xs = take 10 fibs
  mapM_ print xs
  putStrLn $ "10! = " ++ show (fact 10)
"""


def _lexer(cls=TextLexer):
    """Build a lexer with adjacent same-type tokens merged so `->`, `==`, etc.
    survive into a single draw.text() call where HarfBuzz can ligate them."""
    lex = cls()
    lex.add_filter(TokenMergeFilter())
    return lex


FONT_SIZE = 40
CHAR_FONT_SIZE = 72
IMAGE_PAD = 108
LINE_PAD = 12
TARGET_CHARS = 56


# (filename, lexer, code, font_size)
SAMPLES = [
    ("sample_char.png", _lexer(), SAMPLE_CHAR, CHAR_FONT_SIZE),
    ("sample_1.png", _lexer(PythonLexer), SAMPLE_1, FONT_SIZE),
    ("sample_2.png", _lexer(CppLexer), SAMPLE_2, FONT_SIZE),
    ("sample_3.png", _lexer(HaskellLexer), SAMPLE_3, FONT_SIZE),
]


def _target_image_width(font_path):
    """Width of an image holding TARGET_CHARS monospace columns plus padding."""
    font = ImageFont.truetype(font_path, FONT_SIZE)
    char_w = font.getlength("M")
    return int(round(char_w * TARGET_CHARS)) + 2 * IMAGE_PAD


def render_sample(output, lexer, code, font_path, target_width, font_size=FONT_SIZE):
    import io

    bold_path = font_path.replace("-Regular", "-Bold")
    formatter = ImageFormatter(
        font_name=font_path,
        font_name_bold=bold_path if os.path.exists(bold_path) else font_path,
        font_size=font_size,
        line_numbers=False,
        style=GravityNoirStyle,
        image_pad=IMAGE_PAD,
        line_pad=LINE_PAD,
    )
    png_bytes = highlight(code, lexer, formatter)
    rendered = Image.open(io.BytesIO(png_bytes)).convert("RGB")

    if rendered.width > target_width:
        print(
            f"  warning: {output} is {rendered.width}px wide, exceeds target "
            f"{target_width}px — a line is longer than {TARGET_CHARS} chars"
        )
        canvas = rendered
    else:
        canvas = Image.new("RGB", (target_width, rendered.height), BG)
        canvas.paste(rendered, (0, 0))

    os.makedirs(os.path.dirname(output), exist_ok=True)
    canvas.save(output)
    print(f"Saved {output} ({canvas.width}x{canvas.height})")


LES_DRUS_DESCRIPTION = (
    """\
    Les Drus constituent deux pics d'une montagne des Alpes de Haute-Savoie, situés dans le massif du Mont-Blanc:

        — le Grand Dru (3 754 m, point culminant) ;
        — le Petit Dru (3 730 m), qui domine le Montenvers ;

    Les noms des montagnes font partie des couches les plus anciennes des toponymes. La plupart du temps ils sont d'origine celte ou indo-européenne. Selon le linguiste Xavier Delamarre, pour les Celtes, la totalité du monde était symboliquement représentée par un arbre. Dans la langue gauloise, le mot le plus courant pour désigner cet arbre est dru. Les druides étaient ceux qui avaient "la connaissance de l'arbre" (dru, "arbre ou chêne", et uides, "savoir").

    Les Drus se dressent sur l'arête ouest qui descend de l'aiguille Verte. Ils se prolongent par l'arête des Flammes de Pierre. Ils présentent une face nord caractérisée en leur centre par une niche occupée par un névé suspendu ainsi qu'une face sud-est. Leur face ouest, tout en granite, est particulièrement compacte, séparée de la face nord par l'arête nord-ouest qui, avec le pilier sud-ouest (aussi appelé pilier Bonatti), encadre la large face ouest des Drus.

    Comme la plupart des sommets du massif du Mont-Blanc, les roches constituant les Drus sont formées d'une variété de granite appelée protogine.

    Pierre Allain, lors de l'ascension de la face nord des Drus, estima qu'il serait sans doute impossible de gravir un jour le versant ouest. Pourtant, dès 1952, le défi est relevé par A. Dagory, Guido Magnone, Lucien Bérardini et M. Lainé, en deux assauts successifs (1er au 5 juillet puis 17 au 19 juillet 1952). Cette tentative exige l'emploi intensif des techniques de l'escalade artificielle. Dès lors, un nouvel épisode de l'histoire des Drus commence.

    Du 17 au 22 août 1955, l'Italien Walter Bonatti escalade, seul, le pilier sud-ouest avec cinq bivouacs dans la face. Cette ascension est considérée comme un des plus grands exploits de l'histoire de l'alpinisme. En 2001 Jean-Christophe Lafaille ouvre une nouvelle voie en solitaire par la technique de l'escalade artificielle.

    Sept ans après Walter Bonatti, Gary Hemming et Royal Robbins, deux grimpeurs venus des États-Unis, inaugurent une très importante variante menant directement de la base de la face au bloc coincé, dans la moitié supérieure, où elle rejoint la voie de 1952. Ouverte du 24 au 26 juillet 1962, cette voie est baptisée la directe américaine et devint par la suite une grande classique. Ce n'est pas le cas de l'autre directe, toujours américaine, tracée en plein centre de la face par le même Royal Robbins, accompagné cette fois de John Harlin (10 au 13 août 1965). Extrêmement difficile, tant dans le domaine de l'escalade artificielle que de l'escalade libre, cette directissime américaine fut relativement peu répétée.
    """
)


def render_composition(output, font_path, target_width):
    composition_width = target_width * 2
    col_gap = 80
    usable_w = composition_width - 2 * IMAGE_PAD - col_gap
    left_col_w = usable_w * 0.55
    right_col_w = usable_w - left_col_w
    ascii_inner_pad = 80  # padding inside the right column around the ASCII

    title_size = 29

    with open("assets/ascii.txt") as f:
        ascii_lines = f.read().rstrip("\n").splitlines()

    # Auto-size font so the widest ASCII line fits inside the right column with
    # `ascii_inner_pad` of breathing room on each side; the body uses the same
    # size so text and ASCII share visual weight.
    max_ascii_cols = max(len(line) for line in ascii_lines)
    probe = ImageFont.truetype(font_path, 100)
    advance_ratio = probe.getlength("M") / 100
    body_size = int(
        (right_col_w - 2 * ascii_inner_pad) / max_ascii_cols / advance_ratio
    )
    ascii_size = body_size
    body_leading = int(body_size * 1.5)
    ascii_leading = ascii_size + 2

    bold_path = font_path.replace("-Regular", "-Bold")
    title_font = ImageFont.truetype(
        bold_path if os.path.exists(bold_path) else font_path, title_size
    )
    body_font = ImageFont.truetype(font_path, body_size)
    ascii_font = ImageFont.truetype(font_path, ascii_size)

    ascii_char_w = ascii_font.getlength("M")
    ascii_w = int(round(ascii_char_w * max_ascii_cols))
    ascii_h = len(ascii_lines) * ascii_leading

    body_char_w = body_font.getlength("M")
    body_cols = max(20, int(left_col_w // body_char_w))

    import textwrap

    wrapped = []
    for para in LES_DRUS_DESCRIPTION.split("\n"):
        wrapped.extend(textwrap.wrap(para, width=body_cols) or [""])

    title_h = title_size + 32
    body_h = len(wrapped) * body_leading
    left_h = title_h + body_h
    img_h = max(left_h, ascii_h) + 2 * IMAGE_PAD

    img = Image.new("RGB", (composition_width, img_h), BG)
    draw = ImageDraw.Draw(img)

    x = IMAGE_PAD
    y = IMAGE_PAD
    draw.text((x, y), "Les Drus", font=title_font, fill=PRIMARY_BRIGHT)
    y += title_h
    rule_y = y + 16
    draw.line(
        [(x, rule_y), (x + left_col_w, rule_y)],
        fill=PRIMARY_BRIGHT,
        width=2,
    )
    y = rule_y + int(title_h * 0.6)
    for line in wrapped:
        draw.text((x, y), line, font=body_font, fill=FG)
        y += body_leading

    right_col_left = IMAGE_PAD + left_col_w + col_gap
    right_col_h = img_h - 2 * IMAGE_PAD
    ax = right_col_left + (right_col_w - ascii_w) // 2
    ay = IMAGE_PAD + (right_col_h - ascii_h) // 2
    for line in ascii_lines:
        draw.text((ax, ay), line, font=ascii_font, fill=FG)
        ay += ascii_leading

    os.makedirs(os.path.dirname(output), exist_ok=True)
    img.save(output)
    print(f"Saved {output} ({img.width}x{img.height})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate code-sample PNGs")
    parser.add_argument(
        "font",
        nargs="?",
        default="fonts/ttf/NordwandMono-Regular.ttf",
        help="Path to font file",
    )
    parser.add_argument(
        "-o", "--output-dir", default="assets/samples", help="Output directory"
    )
    args = parser.parse_args()

    target_width = _target_image_width(args.font)
    for filename, lexer, code, font_size in SAMPLES:
        render_sample(
            os.path.join(args.output_dir, filename),
            lexer,
            code,
            args.font,
            target_width,
            font_size=font_size,
        )

    render_composition(
        os.path.join(args.output_dir, "les_drus.png"),
        args.font,
        target_width,
    )
