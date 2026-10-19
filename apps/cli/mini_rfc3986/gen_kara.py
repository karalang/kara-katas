# Prints the data section at the end of mini_rfc3986.kara: the files the
# run writes into data/ (the jobs, the webhook registry and the Unicode
# tables) and the source of every pattern the port compiles, taken from
# the vendored rfc3986 itself.
#
# data/ucd.txt is Python's unicodedata and stringprep for the characters
# the jobs can reach (repr's printable test and the nameprep of Python's
# own "idna" codec, IDNA 2003); data/unicode.txt and data/idnadata.txt
# are what the idna package (IDNA 2008) reads, as in mini_idna.
import json, os, re, stringprep, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
sys.path.insert(0, HERE)
ucd32 = unicodedata.ucd_3_2_0

from idna import idnadata  # noqa: E402
import rfc3986.misc as misc  # noqa: E402


def lit(s):
    out = []
    for c in s:
        o = ord(c)
        if c == "\\":
            out.append("\\\\")
        elif c == '"':
            out.append('\\"')
        elif o < 32 or o == 127 or 0xD800 <= o < 0xE000 or not c.isprintable():
            out.append(f"\\u{{{o:x}}}")
        else:
            out.append(c)
    return '"' + "".join(out) + '"'


def chunked(name, text, per=200):
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


def job_strings():
    out = []

    def walk(v):
        if isinstance(v, str):
            out.append(v)
        elif isinstance(v, list):
            for x in v:
                walk(x)
        elif isinstance(v, dict):
            for x in v.values():
                walk(x)

    for line in open(os.path.join(DATA, "jobs.jsonl"), encoding="utf-8"):
        walk(json.loads(line))
    out.append(open(os.path.join(DATA, "webhooks.tsv"), encoding="utf-8").read())
    return out


def decomp_of(ucd, c):
    d = ucd.decomposition(chr(c))
    if not d:
        return "", []
    parts = d.split()
    compat = parts[0].startswith("<")
    if compat:
        parts = parts[1:]
    return ("k" if compat else ""), [int(p, 16) for p in parts]


def ucd_table(strings):
    # w3lib's layout (mini_w3lib): both Unicode versions, printable,
    # stringprep's tables, and the primary composites.
    chars = set(range(128)) | {0xFFFD}
    for s in strings:
        chars.update(map(ord, s))
    out = open(os.path.join(HERE, "expected.out"), encoding="utf-8").read()
    chars.update(map(ord, out))
    for m in re.finditer(r"\\(?:x([0-9a-f]{2})|u([0-9a-f]{4})|U([0-9a-f]{8}))", out):
        chars.add(int(m.group(1) or m.group(2) or m.group(3), 16))
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
    return "\n".join(rows) + "\n"


def idna_tables(strings):
    # mini_idna's layout, for the characters of the IRI hosts (lower-cased
    # as rfc3986 does before idna.encode), closed under decomposition and
    # composition.
    def decomp(cp):
        d = unicodedata.decomposition(chr(cp))
        if not d or d.startswith("<"):
            return []
        return [int(x, 16) for x in d.split()]

    covered = set(range(0x80))
    for s in strings:
        covered.update(ord(c) for c in s)
        covered.update(ord(c) for c in s.lower())
    composites = {}
    for cp in range(0x110000):
        if 0xD800 <= cp < 0xE000:
            continue
        d = decomp(cp)
        if len(d) == 2 and unicodedata.normalize("NFC", chr(cp)) == chr(cp):
            composites.setdefault(d[0], []).append((d[1], cp))
    for li in range(19):
        for vi in range(21):
            lv = 0xAC00 + (li * 21 + vi) * 28
            composites.setdefault(0x1100 + li, []).append((0x1161 + vi, lv))
            for ti in range(1, 28):
                composites.setdefault(lv, []).append((0x11A7 + ti, lv + ti))
    while True:
        more = set()
        for cp in covered:
            if 0xD800 <= cp < 0xE000:
                continue
            more.update(decomp(cp))
            for second, comp in composites.get(cp, []):
                if second in covered:
                    more.add(comp)
        more -= covered
        if not more:
            break
        covered |= more
    uni = ["# cp;ccc;canonical decomposition;flags (p not printable, n no name, c primary composite);bidi;category"]
    for cp in sorted(covered):
        ch = chr(cp)
        if 0xD800 <= cp < 0xE000:
            uni.append("%x;0;;pn;%s;%s" % (cp, unicodedata.bidirectional(ch), unicodedata.category(ch)))
            continue
        d = decomp(cp)
        flags = ("p" if not ch.isprintable() else "") + ("n" if not unicodedata.name(ch, "") else "")
        if len(d) == 2 and unicodedata.normalize("NFC", ch) == ch:
            flags += "c"
        uni.append("%x;%d;%s;%s;%s;%s" % (cp, unicodedata.combining(ch), " ".join("%x" % x for x in d), flags,
                                         unicodedata.bidirectional(ch), unicodedata.category(ch)))

    def ranges(name, rs):
        return ["%s %x %x" % (name, r >> 32, r & 0xFFFFFFFF) for r in rs]

    data = ["# set start end (end exclusive)"]
    for k, v in idnadata.codepoint_classes.items():
        data += ranges(k, v)
    for k, v in idnadata.scripts.items():
        data += ranges("script:" + k, v)
    for k, v in idnadata.joining_types.items():
        data += ranges("joining:" + k, v)
    return "\n".join(uni) + "\n", "\n".join(data) + "\n"


def emit_files():
    strings = job_strings()
    unicode_txt, idnadata_txt = idna_tables(strings)
    files = [
        ("idnadata.txt", idnadata_txt),
        ("jobs.jsonl", open(os.path.join(DATA, "jobs.jsonl"), encoding="utf-8").read()),
        ("ucd.txt", ucd_table(strings)),
        ("unicode.txt", unicode_txt),
        ("webhooks.tsv", open(os.path.join(DATA, "webhooks.tsv"), encoding="utf-8").read()),
    ]
    src = []
    for i, (name, text) in enumerate(files):
        src.append(chunked(f"file_{i}", text))
    src.append("// (path under data/, contents)")
    src.append("fn data_files() -> Vec[(String, String)] {")
    src.append("    let mut v: Vec[(String, String)] = Vec.new();")
    for i, (name, _) in enumerate(files):
        src.append(f"    v.push(({lit(name)}.to_string(), file_{i}()));")
    src.append("    v")
    src.append("}")
    src.append("")
    return "\n".join(src)


def emit_patterns():
    pats = [
        ("subauth", misc.SUBAUTHORITY_MATCHER), ("isubauth", misc.ISUBAUTHORITY_MATCHER),
        ("host", misc.HOST_MATCHER), ("ipv4", misc.IPv4_MATCHER), ("ipv6", misc.IPv6_MATCHER),
        ("ipv6_plain", misc.IPv6_NO_RFC4007_MATCHER), ("path", misc.PATH_MATCHER),
        ("query", misc.QUERY_MATCHER), ("scheme", misc.SCHEME_MATCHER), ("absolute", misc.ABSOLUTE_URI_MATCHER),
    ]
    assert misc.FRAGMENT_MATCHER is misc.QUERY_MATCHER
    out = []
    for name, p in pats:
        out.append(f"fn pat_{name}() -> String {{\n    {lit(p.pattern)}.to_string()\n}}\n")
    return "\n".join(out)


def main():
    print("// ---------------------------------------------------------------- data")
    print("// Generated by gen_kara.py.")
    print()
    print(emit_files())
    print(emit_patterns())


main()
