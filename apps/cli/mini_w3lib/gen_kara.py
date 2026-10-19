# Prints the data section at the end of mini_w3lib.kara: the files the
# run writes into data/, Python's codec registry, the charmap tables of the
# single-byte codecs the port decodes, html.entities.name2codepoint, and
# the Unicode data for every character the jobs can reach.
import codecs, importlib, json, os, re, stringprep, sys, unicodedata
from html.entities import name2codepoint
import encodings, encodings.aliases

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
ucd32 = unicodedata.ucd_3_2_0


def lit(s):
    out = []
    for c in s:
        o = ord(c)
        if c == "\\":
            out.append("\\\\")
        elif c == '"':
            out.append('\\"')
        elif c == "{":
            out.append("{")
        elif o < 32 or o == 127 or 0xD800 <= o < 0xE000 or not c.isprintable():
            out.append(f"\\u{{{o:x}}}")
        else:
            out.append(c)
    return '"' + "".join(out) + '"'


def chunked(name, text, ret="String", per=200):
    # A function building one String from 400-character pieces, split into
    # helpers of at most `per` pieces each.
    pieces = [text[i:i + 400] for i in range(0, len(text), 400)] or [""]
    groups = [pieces[i:i + per] for i in range(0, len(pieces), per)]
    out = []
    for gi, g in enumerate(groups):
        out.append(f"fn {name}_{gi}(out: mut ref String) {{")
        for p in g:
            out.append(f"    out.push_str({lit(p)});")
        out.append("}")
        out.append("")
    out.append(f"fn {name}() -> String {{")
    out.append("    let mut out = String.new();")
    for gi in range(len(groups)):
        out.append(f"    {name}_{gi}(mut out);")
    out.append("    out")
    out.append("}")
    out.append("")
    return "\n".join(out)


def emit_files():
    files = []
    for root, _, names in os.walk(DATA):
        for n in sorted(names):
            p = os.path.join(root, n)
            files.append((os.path.relpath(p, DATA), open(p, "rb").read()))
    files.sort()
    src = []
    for i, (name, body) in enumerate(files):
        try:
            text = body.decode("utf-8")
            binary = "\r" in text and name.endswith(".http")
        except UnicodeDecodeError:
            binary = True
        if binary:
            src.append(chunked(f"file_{i}", body.hex()))
        else:
            src.append(chunked(f"file_{i}", text))
        files[i] = (name, binary)
    src.append("// (path, contents, contents are hex)")
    src.append("fn data_files() -> Vec[(String, String, bool)] {")
    src.append("    let mut v: Vec[(String, String, bool)] = Vec.new();")
    for i, (name, binary) in enumerate(files):
        src.append(f"    v.push(({lit(name)}.to_string(), file_{i}(), {'true' if binary else 'false'}));")
    src.append("    v")
    src.append("}")
    src.append("")
    return "\n".join(src)


def emit_codecs():
    mods = {}
    for f in sorted(os.listdir(os.path.dirname(encodings.__file__))):
        if not f.endswith(".py"):
            continue
        m = f[:-3]
        try:
            mods[m] = importlib.import_module("encodings." + m).getregentry().name
        except Exception:
            pass
    rows = [f"a {k} {v}" for k, v in sorted(encodings.aliases.aliases.items())]
    rows += [f"m {k} {v}" for k, v in sorted(mods.items())]
    return chunked("codec_registry", "\n".join(rows) + "\n")


CHARMAPS = ["cp1252", "cp1251", "iso8859-15"]


def emit_charmaps():
    rows = []
    for name in CHARMAPS:
        cps = []
        for b in range(256):
            try:
                cps.append(f"{ord(bytes([b]).decode(name)):x}")
            except UnicodeDecodeError:
                cps.append("-")
        rows.append(name + " " + " ".join(cps))
    return chunked("charmap_tables", "\n".join(rows) + "\n")


def emit_entities():
    rows = [f"{k} {v:x}" for k, v in sorted(name2codepoint.items())]
    return chunked("entity_table", "\n".join(rows) + "\n")


def collect_chars():
    chars = set(range(128)) | {0xFFFD}

    def walk(v):
        if isinstance(v, dict):
            if "s" in v:
                chars.update(map(ord, v["s"]))
            for x in v.get("l", []):
                walk(x)
            for p in v.get("d", []):
                for x in p:
                    walk(x)

    for line in open(os.path.join(DATA, "jobs.jsonl"), encoding="utf-8"):
        r = json.loads(line)
        for a in r["a"]:
            walk(a)
        for a in r["k"].values():
            walk(a)
    for name in CHARMAPS:
        for b in range(256):
            try:
                chars.add(ord(bytes([b]).decode(name)))
            except UnicodeDecodeError:
                pass
    # Every character the results show, printed or escaped.
    out = open(os.path.join(HERE, "expected.out"), encoding="utf-8").read()
    chars.update(map(ord, out))
    for m in re.finditer(r"\\(?:x([0-9a-f]{2})|u([0-9a-f]{4})|U([0-9a-f]{8}))", out):
        chars.add(int(m.group(1) or m.group(2) or m.group(3), 16))
    site = os.path.join(DATA, "site")
    for n in os.listdir(site):
        body = open(os.path.join(site, n), "rb").read()
        for e in ("utf-8", "utf-16-le", "cp1251", "cp1252", "iso8859-15"):
            chars.update(map(ord, body.decode(e, "replace")))
    return chars


def decomp_of(ucd, c):
    d = ucd.decomposition(chr(c))
    if not d:
        return "", []
    parts = d.split()
    compat = parts[0].startswith("<")
    if compat:
        parts = parts[1:]
    return ("k" if compat else ""), [int(p, 16) for p in parts]


def emit_unicode():
    chars = collect_chars()
    # Close the set under decomposition, case mapping, B.2 and composition.
    canon2 = {}
    for c in range(0x110000):
        if 0xD800 <= c < 0xE000:
            continue
        for tag, ucd in (("c", unicodedata), ("d", ucd32)):
            k, d = decomp_of(ucd, c)
            if not k and len(d) == 2 and ucd.normalize("NFC", chr(c)) == chr(c):
                canon2.setdefault((d[0], d[1]), {})[tag] = c
    while True:
        before = len(chars)
        for c in list(chars):
            ch = chr(c)
            for ucd in (unicodedata, ucd32):
                chars.update(decomp_of(ucd, c)[1])
            chars.update(map(ord, ch.lower()))
            chars.update(map(ord, stringprep.map_table_b2(ch)))
            chars.update(map(ord, unicodedata.normalize("NFKC", ch)))
            chars.update(map(ord, ucd32.normalize("NFKC", ch)))
        for (a, b), comp in canon2.items():
            if a in chars and b in chars:
                chars.update(comp.values())
        if len(chars) == before:
            break
    rows = []
    for c in sorted(chars):
        if 0xD800 <= c < 0xE000:
            continue
        ch = chr(c)
        k1, d1 = decomp_of(unicodedata, c)
        k2, d2 = decomp_of(ucd32, c)
        flags = ""
        if ch.isprintable():
            flags += "p"
        if stringprep.in_table_b1(ch):
            flags += "b"
        if any(f(ch) for f in (stringprep.in_table_c12, stringprep.in_table_c22, stringprep.in_table_c3,
                                stringprep.in_table_c4, stringprep.in_table_c5, stringprep.in_table_c6,
                                stringprep.in_table_c7, stringprep.in_table_c8, stringprep.in_table_c9)):
            flags += "x"
        if stringprep.in_table_d1(ch):
            flags += "r"
        if stringprep.in_table_d2(ch):
            flags += "l"
        b2 = stringprep.map_table_b2(ch)
        b2s = "" if b2 == ch else " ".join(f"{ord(x):x}" for x in b2)
        rows.append(";".join([
            f"{c:x}", str(unicodedata.combining(ch)), k1 + " ".join(f"{x:x}" for x in d1),
            str(ucd32.combining(ch)), k2 + " ".join(f"{x:x}" for x in d2), flags, b2s,
        ]))
    for (a, b), comp in sorted(canon2.items()):
        if a in chars and b in chars:
            for tag, c in sorted(comp.items()):
                rows.append(f"{tag};{a:x};{b:x};{c:x}")
    return chunked("unicode_table", "\n".join(rows) + "\n")


def emit_patterns():
    # The source of every regular expression the port compiles, taken from
    # the vendored modules themselves; "@@" stands for the tag alternation
    # of the patterns w3lib builds per call.
    sys.path.insert(0, HERE)
    import w3lib.html, w3lib.encoding, w3lib._util
    h, e, u = w3lib.html, w3lib.encoding, w3lib._util
    pats = [
        ("ent", h._ent_re.pattern), ("tag", h._tag_re.pattern),
        ("tag_extent", h._tag_extent_re.pattern), ("base", h._base_re.pattern),
        ("base_scan", h._base_scan_re.pattern),
        ("refresh", h._meta_refresh_content_re.pattern), ("tags", h._tags_re.pattern),
        ("meta", h._meta_re.pattern), ("meta_scan", h._meta_scan_source(("@@",))),
        ("meta_scan_none", h._meta_scan_source(())),
        ("comments", h._REMOVECOMMENTS_RE.pattern),
        ("remove_tags", h._build_remove_tags_pattern.__wrapped__(("@@",)).pattern),
        ("attr", u._attr_re.pattern), ("header_enc", e._HEADER_ENCODING_RE.pattern),
        ("header_param", e._HEADER_PARAMETER_RE.pattern),
        ("label", e._ENCODING_LABEL_RE.pattern), ("body_scan", e._BODY_SCAN_RE.pattern),
        ("pragma", e._CONTENT_TYPE_PRAGMA_RE.pattern),
        ("content_charset", e._CONTENT_CHARSET_RE.pattern),
        # the crawl's own, as in oracle.py
        ("title", r"<title>(.*?)</title>"),
        ("href", r"""<a\s[^>]*?href\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))"""),
        ("img", r"""<img\s[^>]*?src\s*=\s*"([^"]*)\""""),
    ]
    out = []
    for name, p in pats:
        out.append(f"fn pat_{name}() -> String {{\n    {lit(p)}.to_string()\n}}\n")
    return "\n".join(out)


def main():
    print("// ---------------------------------------------------------------- data")
    print("// Generated by gen_kara.py.")
    print()
    print(emit_files())
    print(emit_codecs())
    print(emit_charmaps())
    print(emit_entities())
    print(emit_unicode())
    print(emit_patterns())


main()
