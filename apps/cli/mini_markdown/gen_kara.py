# Rewrites the data section at the end of mini_markdown.kara, after the
# MARK line:
# - the regular expressions, as Python-Markdown 3.11.2 compiles them (read
#   from the vendored package's own pattern objects, so each is the exact
#   pattern and flags the library uses), as P_* and F_* constants;
# - html.entities' html5 and codepoint2name tables from this Python;
# - the files under data/ (as mk.py writes them), each file's path under
#   data/ and its text, so the program carries its own inputs.
# Anything outside printable ASCII is written as a \u{...} escape. No
# data function gets more than about 200 lines.
#
# Run from this directory, after mk.py: python3 -I -B gen_kara.py

import unicodedata
import html.entities
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.modules['pygments'] = None
sys.path.insert(0, os.path.join(HERE, 'vendor'))

import markdown  # noqa: E402
from markdown import blockprocessors as bp, inlinepatterns as ip, util, treeprocessors as tp  # noqa: E402
from markdown import postprocessors as pp, preprocessors as prep, serializers, htmlparser  # noqa: E402
from markdown.extensions import abbr, admonition, attr_list, def_list, fenced_code, footnotes  # noqa: E402
from markdown.extensions import legacy_attrs, meta, smarty, tables, toc, wikilinks, sane_lists  # noqa: E402

BS = chr(92)
MARK = "\n// ============================================================ data\n"
KARA = os.path.join(HERE, 'mini_markdown.kara')


def lit(s):
    out = []
    for ch in s:
        if ch == BS:
            out.append(BS + BS)
        elif ch == '"':
            out.append(BS + '"')
        elif ch == "\n":
            out.append(BS + "n")
        elif ch == "\r":
            out.append(BS + "r")
        elif ch == "\t":
            out.append(BS + "t")
        elif " " <= ch <= "~":
            out.append(ch)
        else:
            out.append(BS + "u{%x}" % ord(ch))
    return '"' + "".join(out) + '"'


def read(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return fh.read()


def patterns():
    md = markdown.Markdown()
    parser = md.parser
    hp = htmlparser.htmlparser
    out = []

    def add(name, rx):
        out.append((name, rx.pattern, rx.flags))

    def addp(name, pattern, flags):
        out.append((name, pattern, re.compile(pattern, flags).flags))

    add('INLINE_PH', util.INLINE_PLACEHOLDER_RE)
    add('HTML_PH', util.HTML_PLACEHOLDER_RE)
    addp('NORMALIZE', r'(?<=\n) +\n', 0)
    add('BLOCK_LEVEL', pp.RawHtmlPostprocessor.BLOCK_LEVEL_REGEX)
    base = util.HTML_PLACEHOLDER % r'([0-9]+)'
    addp('RAW_HTML', f'<p>{base}</p>|{base}', 0)
    add('AMP', serializers.RE_AMP)
    add('LIST_INDENT', parser.blockprocessors['indent'].INDENT_RE)
    add('QUOTE', bp.BlockQuoteProcessor.RE)
    ol = parser.blockprocessors['olist']
    add('OL', ol.RE)
    add('OL_CHILD', ol.CHILD_RE)
    add('OL_INDENT', ol.INDENT_RE)
    add('UL', parser.blockprocessors['ulist'].RE)
    addp('INTEGER', r'(\d+)', 0)
    add('HASH', bp.HashHeaderProcessor.RE)
    add('SETEXT', bp.SetextHeaderProcessor.RE)
    add('HR', bp.HRProcessor.SEARCH_RE)
    add('REFERENCE', bp.ReferenceProcessor.RE)
    for name, key in [('BACKTICK', 'backtick'), ('ESCAPE', 'escape'), ('LINK', 'link'),
                      ('IMAGE_LINK', 'image_link'), ('AUTOLINK', 'autolink'), ('AUTOMAIL', 'automail'),
                      ('LINE_BREAK', 'linebreak'), ('HTML', 'html'), ('ENTITY', 'entity')]:
        add(name, md.inlinePatterns[key].compiled_re)
    for token, smart, tag in [('*', False, 'STAR'), ('_', True, 'USMART'), ('_', False, 'UPLAIN')]:
        d = ip.Delimiter(token, 'strong,em', smart, False)
        add('DELIM_%s' % tag, d.boundary)
        add('DELIM_%s_BAD' % tag, d.bad)
    addp('DELIMS_STAR', r'\*', re.DOTALL | re.UNICODE)
    addp('DELIMS_STAR_U', r'\*|_', re.DOTALL | re.UNICODE)
    addp('DELIMS_U', r'_', re.DOTALL | re.UNICODE)
    addp('DELIMS_NONE', r'(?!)', 0)
    add('RE_LINK', ip.LinkInlineProcessor.RE_LINK)
    add('TITLE_CLEAN', ip.LinkInlineProcessor.RE_TITLE_CLEAN)
    add('NEWLINE_CLEANUP', ip.ReferenceInlineProcessor.NEWLINE_CLEANUP_RE)
    add('REF_LINK', ip.ReferenceInlineProcessor.RE_LINK)
    add('UNESCAPE', tp.UnescapeTreeprocessor.RE)
    for name in ['interesting_normal', 'incomplete', 'entityref', 'charref', 'incomplete_charref',
                 'starttagopen', 'endtagopen', 'piclose', 'tagfind_tolerant', 'attrfind_tolerant',
                 'locatetagend', 'endendtag']:
        add('HP_' + name.upper(), getattr(hp, name))
    add('HP_COMMENTCLOSE', htmlparser.commentclose)
    add('BLANK_LINE', htmlparser.blank_line_re)
    add('INNER_BLANK', htmlparser.inner_blank_line_re)
    add('ABBR_DEF', abbr.AbbrBlockprocessor.RE)
    add('ADMONITION', admonition.AdmonitionProcessor.RE)
    add('SPACES', admonition.AdmonitionProcessor.RE_SPACES)
    scanner = [r'[^ =}]+=".*?"', r"[^ =}]+='.*?'", r'[^ =}]+=[^ =}]+', r'[^ =}]+', r' ']
    addp('ATTR_SCAN', '|'.join('(%s)' % s for s in scanner), 0)
    add('NAME', attr_list.NAME_RE)
    add('ATTR_HEADER', attr_list.AttrListTreeprocessor.HEADER_RE)
    add('ATTR_BLOCK', attr_list.AttrListTreeprocessor.BLOCK_RE)
    add('ATTR_INLINE', attr_list.AttrListTreeprocessor.INLINE_RE)
    add('DEF', def_list.DefListProcessor.RE)
    add('DEF_NO_INDENT', def_list.DefListProcessor.NO_INDENT_RE)
    add('FENCED', fenced_code.FencedBlockPreprocessor.FENCED_BLOCK_RE)
    addp('SHEBANG', r'''
            (?:(?:^::+)|(?P<shebang>^[#]!)) # Shebang or 2 or more colons
            (?P<path>(?:/\w+)*[/ ])?        # Zero or 1 path
            (?P<lang>[\w#.+-]*)             # The language
            \s*                             # Arbitrary whitespace
            # Optional highlight lines, single- or double-quote-delimited
            (hl_lines=(?P<quot>"|')(?P<hl_lines>.*?)(?P=quot))?
            ''', re.VERBOSE)
    add('FN_REF_ID', footnotes.RE_REF_ID)
    add('FN_BLOCK', footnotes.FootnoteBlockProcessor.RE)
    addp('FN_INLINE', r'\[\^([^\]]*)\]', re.DOTALL | re.UNICODE)
    add('LEGACY_ATTR', legacy_attrs.ATTR_RE)
    add('META', meta.META_RE)
    add('META_MORE', meta.META_MORE_RE)
    add('META_BEGIN', meta.BEGIN_RE)
    add('META_END', meta.END_RE)
    addp('NL', r'\n', re.DOTALL | re.UNICODE)
    s = sane_lists.SaneListExtension()
    md2 = markdown.Markdown(extensions=[s])
    add('SANE_OL_CHILD', md2.parser.blockprocessors['olist'].CHILD_RE)
    add('SANE_UL_CHILD', md2.parser.blockprocessors['ulist'].CHILD_RE)
    sm = markdown.Markdown(extensions=[smarty.SmartyExtension(smart_angled_quotes=True)])
    reg = sm.treeprocessors['smarty'].inlinePatterns
    for name in [n for n, _ in reg._priority]:
        key = 'SMARTY_' + name[len('smarty-'):].upper().replace('-', '_')
        add(key, reg[name].compiled_re)
    add('HTML_STRICT', sm.inlinePatterns['html'].compiled_re)
    add('TABLE_PIPES', tables.TableProcessor.RE_CODE_PIPES)
    add('TABLE_END_BORDER', tables.TableProcessor.RE_END_BORDER)
    addp('SLUG_STRIP', r'[^\w\s-]', 0)
    addp('SLUG_SEP', r'[{}\s]+'.format('-'), 0)
    add('IDCOUNT', toc.IDCOUNT_RE)
    addp('HEADER_TAG', '[Hh][123456]', 0)
    addp('WIKILINK', r'\[\[([\w0-9_ -]+)\]\]', re.DOTALL | re.UNICODE)
    addp('WIKI_URL', r'([ ]+_)|(_[ ]+)|([ ]+)', 0)
    return out


def smarty_order():
    sm = markdown.Markdown(extensions=[smarty.SmartyExtension(smart_angled_quotes=True)])
    reg = sm.treeprocessors['smarty'].inlinePatterns
    return [(n, p) for n, p in reg._priority]


def entity_lines():
    lines = []
    items = sorted(html.entities.html5.items())
    chunks = [items[i:i + 200] for i in range(0, len(items), 200)]
    lines += ["", "// html.entities.html5: the names html.unescape knows, with and",
              "// without a final ';'.", "fn html5_entities() -> Map[String, String] {",
              "    let mut m: Map[String, String] = Map.new();"]
    for k in range(len(chunks)):
        lines.append("    add_entities_%d(mut m);" % k)
    lines += ["    m", "}"]
    for k, chunk in enumerate(chunks):
        lines += ["", "fn add_entities_%d(m: mut ref Map[String, String]) {" % k]
        for name, value in chunk:
            lines.append("    m.insert(%s.to_string(), %s.to_string());" % (lit(name), lit(value)))
        lines.append("}")
    lines += ["", "// html.entities.codepoint2name: HTML 4's names, for the e-mail",
              "// autolink's obfuscation.", "fn codepoint_names() -> Map[i64, String] {",
              "    let mut m: Map[i64, String] = Map.new();"]
    for cp, name in sorted(html.entities.codepoint2name.items()):
        lines.append("    m.insert(%d, %s.to_string());" % (cp, lit(name)))
    lines += ["    m", "}"]
    # toc's slugify keeps the ASCII part of each character's NFKD form;
    # combining marks are never ASCII, so per-character is exact.
    pairs = []
    for cp in range(0x80, 0x110000):
        a = unicodedata.normalize('NFKD', chr(cp)).encode('ascii', 'ignore').decode('ascii')
        if a:
            pairs.append((cp, a))
    chunks = [pairs[i:i + 300] for i in range(0, len(pairs), 300)]
    lines += ["", "// unicodedata.normalize('NFKD', c) with the non-ASCII dropped, for",
              "// every non-ASCII character that keeps something (Unicode %s)." % unicodedata.unidata_version,
              "fn nfkd_ascii() -> Map[i64, String] {",
              "    let mut m: Map[i64, String] = Map.new();"]
    for k in range(len(chunks)):
        lines.append("    add_nfkd_%d(mut m);" % k)
    lines += ["    m", "}"]
    for k, chunk in enumerate(chunks):
        lines += ["", "fn add_nfkd_%d(m: mut ref Map[i64, String]) {" % k]
        for cp, a in chunk:
            lines.append("    m.insert(%d, %s.to_string());" % (cp, lit(a)))
        lines.append("}")
    return lines


def main():
    src = read(KARA)
    src = src[:src.index(MARK)]
    d = [""]
    for name, pattern, flags in patterns():
        d.append("const P_%s: Str = %s;" % (name, lit(pattern)))
        d.append("const F_%s: i64 = %d;" % (name, flags))
    d += entity_lines()
    names = []
    for root, dirs, files in os.walk(os.path.join(HERE, "data")):
        for f in files:
            names.append(os.path.relpath(os.path.join(root, f), os.path.join(HERE, "data")))
    names = sorted(n for n in names if not n.startswith('out' + os.sep))
    d += ["", "// The files under data/, in path order. Each body is built by",
          "// a run of functions, a few kilobytes of text apiece.",
          "fn data_files() -> Vec[DataFile] {",
          "    let mut v: Vec[DataFile] = Vec.new();"]
    funcs = []
    for idx, n in enumerate(names):
        text = read(os.path.join(HERE, "data", n))
        pieces = []
        cur = ''
        for line in text.splitlines(keepends=True):
            if cur and len(cur) + len(line) > 1500:
                pieces.append(cur)
                cur = ''
            cur += line
        if cur:
            pieces.append(cur)
        groups = [pieces[i:i + 40] for i in range(0, len(pieces), 40)] or [[]]
        d.append("    let mut t%d = String.new();" % idx)
        for k, g in enumerate(groups):
            d.append("    data_%d_%d(mut t%d);" % (idx, k, idx))
            body = ["", "fn data_%d_%d(t: mut ref String) {" % (idx, k)]
            for piece in g:
                body.append("    t.push_str(%s);" % lit(piece))
            body.append("}")
            funcs += body
        d.append("    v.push(DataFile { path: %s.to_string(), body: t%d });" % (lit(n), idx))
    d += ["    v", "}"]
    d += funcs
    with open(KARA, "w", encoding="utf-8", newline="") as fh:
        fh.write(src + MARK + "\n".join(d) + "\n")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--smarty-order':
        for n, p in smarty_order():
            print(n, p)
    else:
        main()
