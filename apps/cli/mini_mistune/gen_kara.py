# Prints two sections of mini_mistune.kara:
# - the regular expressions, read from the copy of mistune in mistune/,
#   so the port uses mistune's own patterns, character for character;
# - the functions that hold data/ (as mk.py writes it): each file's path
#   under data/ and its text. No function gets more than about 200 lines.
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
os.chdir(HERE)

from mistune import block_parser, core, helpers, inline_parser, list_parser, util  # noqa: E402
from mistune.directives import _fenced, _rst, image  # noqa: E402
from mistune.plugins import (  # noqa: E402
    abbr, def_list, footnotes, formatting, math, ruby, speedup, spoiler, table, task_lists, url,
)
from mistune.renderers import markdown as md_renderer  # noqa: E402


def lit(s):
    out = []
    for ch in s:
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        elif ord(ch) < 32 or ord(ch) > 126:
            out.append("\\u{%x}" % ord(ch))
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


# Compiled patterns: (field, compiled regex).
COMPILED = [
    ("line_end", core._LINE_END),
    ("expand_tab", util._expand_tab_re),
    ("charref", util._charref_re),
    ("striptags", util._striptags_re),
    ("strip_end", util._strip_end_re),
    ("link_bracket_start", helpers.LINK_BRACKET_START),
    ("link_bracket", helpers.LINK_BRACKET_RE),
    ("link_href_block", helpers.LINK_HREF_BLOCK_RE),
    ("link_href_inline", helpers.LINK_HREF_INLINE_RE),
    ("link_title", helpers.LINK_TITLE_RE),
    ("paren_end", helpers.PAREN_END_RE),
    ("inline_link_label", helpers._INLINE_LINK_LABEL_RE),
    ("inline_square_bracket", helpers._INLINE_SQUARE_BRACKET_RE),
    ("escape_char", helpers._ESCAPE_CHAR_RE),
    ("indent_code_trim", block_parser._INDENT_CODE_TRIM),
    ("axt_heading_trim", block_parser._AXT_HEADING_TRIM),
    ("block_quote_trim", block_parser._BLOCK_QUOTE_TRIM),
    ("block_quote_leading", block_parser._BLOCK_QUOTE_LEADING),
    ("line_blank_end", block_parser._LINE_BLANK_END),
    ("blank_to_line", block_parser._BLANK_TO_LINE),
    ("open_tag_end", block_parser._OPEN_TAG_END),
    ("close_tag_end", block_parser._CLOSE_TAG_END),
    ("strict_block_quote", block_parser._STRICT_BLOCK_QUOTE),
    ("blank_line", block_parser.BlockParser.BLANK_LINE),
    ("line_has_text", list_parser._LINE_HAS_TEXT),
    ("em1", inline_parser.EMPHASIS_END_RE["*"]),
    ("em_1", inline_parser.EMPHASIS_END_RE["_"]),
    ("em2", inline_parser.EMPHASIS_END_RE["**"]),
    ("em_2", inline_parser.EMPHASIS_END_RE["__"]),
    ("em3", inline_parser.EMPHASIS_END_RE["***"]),
    ("em_3", inline_parser.EMPHASIS_END_RE["___"]),
    ("hard_linebreak", speedup.HARD_LINEBREAK_RE),
    ("strike_end", formatting._STRIKE_END),
    ("mark_end", formatting._MARK_END),
    ("insert_end", formatting._INSERT_END),
    ("table_cell", table.TABLE_CELL),
    ("cell_split", table.CELL_SPLIT),
    ("align_center", table.ALIGN_CENTER),
    ("align_left", table.ALIGN_LEFT),
    ("align_right", table.ALIGN_RIGHT),
    ("paragraph_split", footnotes._PARAGRAPH_SPLIT),
    ("task_list_item", task_lists.TASK_LIST_ITEM),
    ("def_re", def_list.DEF_RE),
    ("dd_start", def_list.DD_START_RE),
    ("def_trim", def_list.TRIM_RE),
    ("has_blank_line", def_list.HAS_BLANK_LINE_RE),
    ("ruby", ruby._ruby_re),
    ("spoiler_start", spoiler._BLOCK_SPOILER_START),
    ("spoiler_match", spoiler._BLOCK_SPOILER_MATCH),
    ("fenced_type", _fenced._type_re),
    ("fenced_directive", _fenced._directive_re),
    ("rst_directive", _rst._directive_re),
    ("num", image._num_re),
    ("fenced_marker", md_renderer.fenced_re),
]

# Pattern text that rules are made of: (function, text).
TEXTS = [
    ("prevent_backslash", helpers.PREVENT_BACKSLASH),
    ("link_label", helpers.LINK_LABEL),
    ("speedup_paragraph", speedup.PARAGRAPH),
    ("superscript", formatting.SUPERSCRIPT_PATTERN),
    ("subscript", formatting.SUBSCRIPT_PATTERN),
    ("table", table.TABLE_PATTERN),
    ("nptable", table.NP_TABLE_PATTERN),
    ("ref_footnote", footnotes.REF_FOOTNOTE),
    ("inline_footnote", footnotes.INLINE_FOOTNOTE),
    ("url_link", url.URL_LINK_PATTERN),
    ("ref_abbr", abbr.REF_ABBR),
    ("def_list", def_list.DEF_PATTERN),
    ("block_math", math.BLOCK_MATH_PATTERN),
    ("inline_math", math.INLINE_MATH_PATTERN),
    ("inline_spoiler", spoiler.INLINE_SPOILER_PATTERN),
    ("rst_directive_start", _rst.RSTDirective.directive_pattern),
    ("std_linebreak", inline_parser.InlineParser.STD_LINEBREAK),
    ("hard_linebreak_rule", inline_parser.InlineParser.HARD_LINEBREAK),
]


def patterns():
    print("// ------------------------------------------------------------ patterns")
    print()
    print("// mistune's regular expressions, as gen_kara.py read them from")
    print("// mistune/. The flags are re's: 8 is MULTILINE, 16 DOTALL, 32 UNICODE.")
    print("struct Pats {")
    for name, _ in COMPILED:
        print("    %s: i64," % name)
    print("}")
    print()
    print("fn make_pats(rx: mut ref Rx) -> Pats {")
    print("    Pats {")
    for name, r in COMPILED:
        print("        %s: rx_id(rx, %s, %d)," % (name, lit(r.pattern), r.flags))
    print("    }")
    print("}")
    for name, text in TEXTS:
        print()
        print("fn pat_%s() -> Str {" % name)
        print("    %s" % lit(text))
        print("}")
    for title, spec in (("block", block_parser.BlockParser.SPECIFICATION),
                        ("inline", inline_parser.InlineParser.SPECIFICATION)):
        print()
        print("// %sParser.SPECIFICATION." % title.capitalize())
        print("fn %s_spec() -> Vec[(String, Vec[i64])] {" % title)
        print("    let mut v: Vec[(String, Vec[i64])] = Vec.new();")
        for k, p in spec.items():
            print("    v.push((%s.to_string(), u(%s)));" % (lit(k), lit(p)))
        print("    v")
        print("}")
    for title, rules in (("block", block_parser.BlockParser.DEFAULT_RULES),
                         ("inline", inline_parser.InlineParser.DEFAULT_RULES)):
        print()
        print("fn %s_default_rules() -> Vec[String] {" % title)
        print("    let mut v: Vec[String] = Vec.new();")
        for k in rules:
            print("    v.push(%s.to_string());" % lit(k))
        print("    v")
        print("}")
    for name, tags in (("block_tags", helpers.BLOCK_TAGS), ("pre_tags", helpers.PRE_TAGS)):
        print()
        print("fn %s() -> Vec[String] {" % name)
        print("    let mut v: Vec[String] = Vec.new();")
        for k in tags:
            print("    v.push(%s.to_string());" % lit(k))
        print("    v")
        print("}")
    print()
    print("fn punctuation() -> Str {")
    print("    %s" % lit(helpers.PUNCTUATION))
    print("}")


def is_text(b):
    try:
        s = b.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return all(c >= " " or c in "\n\t" for c in s)


def datafiles():
    names = []
    for root, dirs, files in os.walk("data"):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), "data")
            if not rel.startswith("out" + os.sep):
                names.append(rel)
    names.sort()
    chunks = [[]]
    for n in names:
        b = open(os.path.join("data", n), "rb").read()
        assert is_text(b), n
        body = ["    let mut t = String.new();"]
        for line in b.decode("utf-8").splitlines(keepends=True):
            body.append("    t.push_str(%s);" % lit(line))
        body.append("    v.push(DataFile { path: %s.to_string(), body: t });" % lit(n))
        if len(chunks[-1]) + len(body) > 190 and chunks[-1]:
            chunks.append([])
        chunks[-1].extend(body)
    print("// ------------------------------------------------------------ data")
    print()
    print("// The files under data/, in path order.")
    print("fn data_files() -> Vec[DataFile] {")
    print("    let mut v: Vec[DataFile] = Vec.new();")
    for k in range(len(chunks)):
        print("    data_part_%d(mut v);" % k)
    print("    v")
    print("}")
    for k, body in enumerate(chunks):
        print()
        print("fn data_part_%d(v: mut ref Vec[DataFile]) {" % k)
        for line in body:
            print(line)
        print("}")


if sys.argv[1:] == ["patterns"]:
    patterns()
else:
    datafiles()
