# Reference: runs the css-parsing-tests suites in data/ through the
# vendored tinycss2 (as tinycss2's own tests/test_tinycss2.py does), then
# audits the stylesheets in data/sheets/. Prints every case as
# "<suite> <i>: <json>", or "<suite> <i>: raised <Type>: <first argument>".
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
sys.path.insert(0, HERE)

from webencodings import Encoding, lookup  # noqa: E402
from tinycss2 import (  # noqa: E402
    parse_blocks_contents, parse_component_value_list, parse_declaration_list,
    parse_one_component_value, parse_one_declaration, parse_one_rule,
    parse_rule_list, parse_stylesheet, parse_stylesheet_bytes, serialize)
from tinycss2.ast import (  # noqa: E402
    AtKeywordToken, AtRule, Comment, CurlyBracketsBlock, Declaration,
    DimensionToken, FunctionBlock, HashToken, IdentToken, LiteralToken,
    NumberToken, ParenthesesBlock, ParseError, PercentageToken, QualifiedRule,
    SquareBracketsBlock, StringToken, UnicodeRangeToken, URLToken,
    WhitespaceToken)
from tinycss2.color3 import RGBA  # noqa: E402
from tinycss2.color3 import parse_color as parse_color3  # noqa: E402
from tinycss2.color4 import parse_color as parse_color4  # noqa: E402
from tinycss2.nth import parse_nth  # noqa: E402
from tinycss2.serializer import serialize_identifier  # noqa: E402


# ---------------------------------------------------------------- tests

def numeric(t):
    return [t.representation, t.value, "integer" if t.int_value is not None else "number"]


def to_json(v):
    if v is None:
        return None
    if isinstance(v, (str, int)) and not isinstance(v, bool):
        return v
    if isinstance(v, (list, tuple)) and not isinstance(v, RGBA):
        return [to_json(x) for x in v]
    if isinstance(v, Encoding):
        return v.name
    if isinstance(v, ParseError):
        return ["error", v.kind]
    if isinstance(v, Comment):
        return "/* … */"
    if isinstance(v, WhitespaceToken):
        return " "
    if isinstance(v, LiteralToken):
        return v.value
    if isinstance(v, IdentToken):
        return ["ident", v.value]
    if isinstance(v, AtKeywordToken):
        return ["at-keyword", v.value]
    if isinstance(v, HashToken):
        return ["hash", v.value, "id" if v.is_identifier else "unrestricted"]
    if isinstance(v, StringToken):
        return ["string", v.value]
    if isinstance(v, URLToken):
        return ["url", v.value]
    if isinstance(v, NumberToken):
        return ["number", *numeric(v)]
    if isinstance(v, PercentageToken):
        return ["percentage", *numeric(v)]
    if isinstance(v, DimensionToken):
        return ["dimension", *numeric(v), v.unit]
    if isinstance(v, UnicodeRangeToken):
        return ["unicode-range", v.start, v.end]
    if isinstance(v, CurlyBracketsBlock):
        return ["{}", *to_json(v.content)]
    if isinstance(v, SquareBracketsBlock):
        return ["[]", *to_json(v.content)]
    if isinstance(v, ParenthesesBlock):
        return ["()", *to_json(v.content)]
    if isinstance(v, FunctionBlock):
        return ["function", v.name, *to_json(v.arguments)]
    if isinstance(v, Declaration):
        return ["declaration", v.name, to_json(v.value), v.important]
    if isinstance(v, AtRule):
        return ["at-rule", v.at_keyword, to_json(v.prelude), to_json(v.content)]
    if isinstance(v, QualifiedRule):
        return ["qualified rule", to_json(v.prelude), to_json(v.content)]
    if isinstance(v, RGBA):
        return [round(c, 6) for c in v]
    raise TypeError(type(v).__name__)


SKIP = {"skip_comments": True, "skip_whitespace": True}


def _number(value):
    if value is None:
        return "none"
    value = round(value + 0.0000001, 6)
    return str(int(value) if value.is_integer() else value)


def rgb_string(color):
    (*coordinates, alpha) = color
    result = f'rgb{"a" if alpha != 1 else ""}('
    result += ", ".join(_number(coordinate * 255) for coordinate in coordinates)
    if alpha != 1:
        result += f", {_number(alpha)}"
    return result + ")"


def space_string(color):
    (*coordinates, alpha) = color
    result = f"{color.space}("
    result += " ".join(_number(coordinate) for coordinate in coordinates)
    if alpha != 1:
        result += f" / {_number(alpha)}"
    return result + ")"


def t_function_4(css):
    if not (color := parse_color4(css)):
        return None
    (*coordinates, alpha) = color
    result = f"color({color.space}"
    for coordinate in coordinates:
        result += f" {_number(coordinate)}"
    if alpha != 1:
        result += f" / {_number(alpha)}"
    return result + ")"


def t_rgb3(css):
    if not (color := parse_color3(css)):
        return None
    if isinstance(color, str):
        return color
    return rgb_string(color)


def t_rgb4(space, convert):
    def run(css):
        if not (color := parse_color4(css)):
            return None
        if isinstance(color, str):
            return color
        assert color.space == space
        return rgb_string(color.to("srgb") if convert else color)
    return run


def t_space4(space):
    def run(css):
        if not (color := parse_color4(css)):
            return None
        if isinstance(color, str):
            return color
        assert color.space == space
        return space_string(color)
    return run


def t_bytes(kwargs):
    kwargs = dict(kwargs)
    kwargs["css_bytes"] = kwargs["css_bytes"].encode("latin1")
    kwargs.pop("comment", None)
    if kwargs.get("environment_encoding"):
        kwargs["environment_encoding"] = lookup(kwargs["environment_encoding"])
    kwargs.update(SKIP)
    return parse_stylesheet_bytes(**kwargs)


def t_serialization(css):
    parsed = parse_component_value_list(css, skip_comments=True)
    return parse_component_value_list(serialize(parsed), skip_comments=True)


SUITES = [
    ("component_value_list", "component_value_list.json", lambda c: parse_component_value_list(c, skip_comments=True)),
    ("one_component_value", "one_component_value.json", lambda c: parse_one_component_value(c, skip_comments=True)),
    ("declaration_list", "declaration_list.json", lambda c: parse_declaration_list(c, **SKIP)),
    ("blocks_contents", "blocks_contents.json", lambda c: parse_blocks_contents(c, **SKIP)),
    ("one_declaration", "one_declaration.json", lambda c: parse_one_declaration(c, skip_comments=True)),
    ("stylesheet", "stylesheet.json", lambda c: parse_stylesheet(c, **SKIP)),
    ("rule_list", "rule_list.json", lambda c: parse_rule_list(c, **SKIP)),
    ("one_rule", "one_rule.json", lambda c: parse_one_rule(c, skip_comments=True)),
    ("nth", "An+B.json", parse_nth),
    ("color_function_4", "color_function_4.json", t_function_4),
    ("color_hexadecimal_3", "color_hexadecimal_3.json", t_rgb3),
    ("color_hexadecimal_4", "color_hexadecimal_4.json", t_rgb4("srgb", False)),
    ("color_hexadecimal_3_with_4", "color_hexadecimal_3.json", t_rgb4("srgb", False)),
    ("color_hsl_3", "color_hsl_3.json", t_rgb3),
    ("color_hsl_3_with_4", "color_hsl_3.json", t_rgb4("hsl", True)),
    ("color_hsl_4", "color_hsl_4.json", t_rgb4("hsl", True)),
    ("color_hwb_4", "color_hwb_4.json", t_rgb4("hwb", True)),
    ("color_keywords_3", "color_keywords_3.json", t_rgb3),
    ("color_keywords_3_with_4", "color_keywords_3.json", t_rgb4("srgb", False)),
    ("color_keywords_4", "color_keywords_4.json", t_rgb4("srgb", False)),
    ("color_lab_4", "color_lab_4.json", t_space4("lab")),
    ("color_oklab_4", "color_oklab_4.json", t_space4("oklab")),
    ("color_lch_4", "color_lch_4.json", t_space4("lch")),
    ("color_oklch_4", "color_oklch_4.json", t_space4("oklch")),
    ("stylesheet_bytes", "stylesheet_bytes.json", t_bytes),
    ("serialization", "component_value_list.json", t_serialization),
]


def run_suites(out):
    total = same = 0
    for name, filename, function in SUITES:
        with open(os.path.join(DATA, filename), encoding="utf-8") as f:
            data = json.load(f)
        cases = list(zip(data[::2], data[1::2]))
        matched = 0
        for i, (css, expected) in enumerate(cases, 1):
            try:
                value = to_json(function(css))
                text = json.dumps(value)
                if value == expected:
                    matched += 1
            except Exception as e:
                text = "raised %s: %s" % (type(e).__name__, e.args[0] if e.args else "")
            out.append("%s %d: %s" % (name, i, text))
        out.append("== %s: %d cases, %d as expected" % (name, len(cases), matched))
        total += len(cases)
        same += matched
    out.append("== suites: %d cases, %d as expected" % (total, same))


# ---------------------------------------------------------------- audit

NTH = ("nth-child", "nth-last-child", "nth-of-type", "nth-last-of-type")
RULE_BLOCKS = ("media", "supports", "layer", "document", "container", "keyframes")


def trim(tokens):
    tokens = list(tokens)
    while tokens and tokens[0].type in ("whitespace", "comment"):
        tokens.pop(0)
    while tokens and tokens[-1].type in ("whitespace", "comment"):
        tokens.pop()
    return tokens


def channel_byte(v):
    return int(max(0.0, min(255.0, math.floor(v * 255 + 0.5))))


def describe(color):
    if isinstance(color, str):
        return color, None
    if color.space in ("srgb", "hsl", "hwb"):
        s = color.to("srgb")
        hexs = "#" + "".join("%02x" % channel_byte(c) for c in s.coordinates)
        if s.alpha != 1:
            hexs += "%02x" % channel_byte(s.alpha)
        return hexs, s
    if color.space in ("lab", "lch", "oklab", "oklch", "xyz-d50", "xyz-d65"):
        return space_string(color.to("lab")), None
    return "%s (not converted)" % color.space, None


def luminance(s):
    lin = []
    for c in s.coordinates:
        lin.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def find_colors(tokens, found):
    for t in tokens:
        if t.type in ("ident", "hash", "function"):
            c = parse_color4(t)
            if c is not None:
                found.append(c)
                continue
        if t.type == "function":
            find_colors(t.arguments, found)
        elif t.type in ("() block", "[] block"):
            find_colors(t.content, found)


def find_urls(tokens, found):
    for t in tokens:
        if t.type == "url":
            found.append(t.value)
        elif t.type == "function":
            if t.lower_name == "url":
                args = trim(t.arguments)
                if len(args) == 1 and args[0].type == "string":
                    found.append(args[0].value)
            else:
                find_urls(t.arguments, found)
        elif t.type in ("() block", "[] block", "{} block"):
            find_urls(t.content, found)


def find_vars(tokens, found):
    for t in tokens:
        if t.type == "function":
            if t.lower_name == "var":
                args = trim(t.arguments)
                if args and args[0].type == "ident":
                    found.append(args[0].value)
            find_vars(t.arguments, found)
        elif t.type in ("() block", "[] block"):
            find_vars(t.content, found)


def find_errors(tokens, found):
    for t in tokens:
        if t.type == "error":
            found.append(t)
        elif t.type == "function":
            find_errors(t.arguments, found)
        elif t.type in ("() block", "[] block", "{} block"):
            find_errors(t.content, found)


def nth_examples(a, b):
    seen = []
    for n in range(0, 40):
        i = a * n + b
        if i >= 1 and i not in seen:
            seen.append(i)
    seen.sort()
    return seen[:6]


def find_nth(tokens, out, ind):
    for t in tokens:
        if t.type == "function":
            if t.lower_name in NTH:
                r = parse_nth(t.arguments)
                arg = serialize(trim(t.arguments))
                if r is None:
                    out.append("%s:%s(%s) is not a valid An+B" % (ind, t.name, arg))
                else:
                    a, b = r
                    out.append("%s:%s(%s) a=%d b=%d matches %s" % (
                        ind, t.name, arg, a, b, ", ".join(str(i) for i in nth_examples(a, b)) or "nothing"))
            find_nth(t.arguments, out, ind)
        elif t.type in ("() block", "[] block"):
            find_nth(t.content, out, ind)


class Sheet:
    def __init__(self):
        self.rules = 0
        self.declarations = 0
        self.important = 0
        self.defined = []
        self.used = []
        self.urls = []
        self.errors = 0
        self.low_contrast = 0


def winner(decls, name):
    best = None
    for d in decls:
        if d.lower_name == name and (best is None or d.important or not best.important):
            best = d
    return best


def single_color(d):
    if d is None:
        return None
    vals = trim(d.value)
    if len(vals) != 1:
        return None
    c = parse_color4(vals[0])
    if c is None or isinstance(c, str):
        return None
    _, s = describe(c)
    if s is None or s.alpha != 1:
        return None
    return s


def audit_declarations(sheet, nodes, out, ind, palette):
    decls = []
    seen = {}
    for d in nodes:
        if d.type == "error":
            sheet.errors += 1
            out.append("%s%d:%d error %s: %s" % (ind, d.source_line, d.source_column, d.kind, d.message))
            continue
        if d.type != "declaration":
            out.append("%snested %s at %d:%d" % (ind, d.type, d.source_line, d.source_column))
            continue
        sheet.declarations += 1
        decls.append(d)
        value = serialize(trim(d.value))
        line = "%s%s: %s" % (ind, d.name, value)
        if d.important:
            sheet.important += 1
            line += " !important"
        out.append(line)
        if d.lower_name in seen:
            out.append("%s  duplicate of line %d" % (ind, seen[d.lower_name]))
        seen[d.lower_name] = d.source_line
        if d.name.startswith("--"):
            sheet.defined.append(d.name)
        colors = []
        find_colors(d.value, colors)
        for c in colors:
            text, _ = describe(c)
            palette[text] = palette.get(text, 0) + 1
            out.append("%s  color %s" % (ind, text))
        if d.lower_name == "unicode-range":
            total = 0
            n = 0
            for t in d.value:
                if t.type == "unicode-range":
                    n += 1
                    total += t.end - t.start + 1
            out.append("%s  %d ranges, %d code points" % (ind, n, total))
        find_urls(d.value, sheet.urls)
        find_vars(d.value, sheet.used)
        errs = []
        find_errors(d.value, errs)
        for e in errs:
            sheet.errors += 1
            out.append("%s  %d:%d error %s: %s" % (ind, e.source_line, e.source_column, e.kind, e.message))
    fg = single_color(winner(decls, "color"))
    bg = single_color(winner(decls, "background-color"))
    if bg is None:
        bg = single_color(winner(decls, "background"))
    if fg is not None and bg is not None:
        l1, l2 = luminance(fg), luminance(bg)
        if l1 < l2:
            l1, l2 = l2, l1
        ratio = (l1 + 0.05) / (l2 + 0.05)
        verdict = "AAA" if ratio >= 7 else "AA" if ratio >= 4.5 else "AA large" if ratio >= 3 else "FAIL"
        if verdict in ("FAIL", "AA large"):
            sheet.low_contrast += 1
        out.append("%scontrast %.2f:1 %s" % (ind, ratio, verdict))


def audit_rules(sheet, rules, out, ind, palette):
    for r in rules:
        if r.type == "error":
            sheet.errors += 1
            out.append("%s%d:%d error %s: %s" % (ind, r.source_line, r.source_column, r.kind, r.message))
            continue
        sheet.rules += 1
        prelude = serialize(trim(r.prelude))
        if r.type == "at-rule":
            kw = r.lower_at_keyword
            out.append("%s%d:%d @%s %s%s" % (ind, r.source_line, r.source_column, r.at_keyword, prelude,
                                           ";" if r.content is None else " {"))
            if kw == "import":
                find_urls(r.prelude, sheet.urls)
                first = trim(r.prelude)
                if first and first[0].type == "string":
                    sheet.urls.append(first[0].value)
            if r.content is None:
                continue
            if kw in RULE_BLOCKS:
                audit_rules(sheet, parse_rule_list(r.content, **SKIP), out, ind + "  ", palette)
            else:
                audit_declarations(sheet, parse_blocks_contents(r.content, **SKIP), out, ind + "  ", palette)
            out.append(ind + "}")
        else:
            out.append("%s%d:%d %s {" % (ind, r.source_line, r.source_column, prelude))
            find_nth(r.prelude, out, ind + "  ")
            errs = []
            find_errors(r.prelude, errs)
            for e in errs:
                sheet.errors += 1
                out.append("%s  %d:%d error %s: %s" % (ind, e.source_line, e.source_column, e.kind, e.message))
            audit_declarations(sheet, parse_blocks_contents(r.content, **SKIP), out, ind + "  ", palette)
            out.append(ind + "}")


def minify_declarations(nodes):
    parts = []
    for d in nodes:
        if d.type == "declaration":
            parts.append(serialize_identifier(d.name) + ":" + serialize(trim(d.value)) +
                         ("!important" if d.important else ""))
        elif d.type == "qualified-rule":
            parts.append(minify([d]))
    return ";".join(parts)


def minify(rules):
    out = []
    for r in rules:
        if r.type == "qualified-rule":
            out.append(serialize(trim(r.prelude)) + "{" +
                       minify_declarations(parse_blocks_contents(r.content, **SKIP)) + "}")
        elif r.type == "at-rule":
            prelude = serialize(trim(r.prelude))
            head = "@" + serialize_identifier(r.at_keyword) + (" " + prelude if prelude else "")
            if r.content is None:
                out.append(head + ";")
            elif r.lower_at_keyword in RULE_BLOCKS:
                out.append(head + "{" + minify(parse_rule_list(r.content, **SKIP)) + "}")
            else:
                out.append(head + "{" + minify_declarations(parse_blocks_contents(r.content, **SKIP)) + "}")
    return "".join(out)


def audit(out):
    palette = {}
    with open(os.path.join(DATA, "sheets", "sheets.tsv"), encoding="utf-8") as f:
        rows = [l.rstrip("\n").split("\t") for l in f if l.strip()]
    for name, protocol, environment in rows:
        with open(os.path.join(DATA, "sheets", name), "rb") as f:
            data = f.read()
        rules, encoding = parse_stylesheet_bytes(
            data, protocol_encoding=protocol or None,
            environment_encoding=lookup(environment) if environment else None, **SKIP)
        out.append("== sheet %s: %d bytes, %s" % (name, len(data), encoding.name))
        sheet = Sheet()
        audit_rules(sheet, rules, out, "  ", palette)
        undefined = []
        for v in sheet.used:
            if v not in sheet.defined and v not in undefined:
                undefined.append(v)
        out.append("  %d rules, %d declarations (%d !important), %d errors, %d low-contrast pairs" % (
            sheet.rules, sheet.declarations, sheet.important, sheet.errors, sheet.low_contrast))
        out.append("  custom properties: %d defined, %d used, undefined: %s" % (
            len(sheet.defined), len(sheet.used), ", ".join(undefined) or "none"))
        out.append("  urls: %s" % (", ".join(json.dumps(u) for u in sheet.urls) or "none"))
        text = minify(rules)
        out.append("  minified to %d characters" % len(text))
        if len(text) <= 400:
            out.append("  " + text)
    out.append("== palette")
    for text, n in sorted(palette.items(), key=lambda kv: (-kv[1], kv[0])):
        out.append("  %3d %s" % (n, text))


def main():
    out = []
    run_suites(out)
    audit(out)
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
