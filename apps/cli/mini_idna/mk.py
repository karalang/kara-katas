# Writes data/: the jobs (data/jobs.jsonl), idna's own tables for the
# characters the jobs can reach (data/uts46.txt, data/idnadata.txt), and
# what Python's unicodedata (Unicode 15.1 in Python 3.13) says about those
# characters (data/unicode.txt).
import bisect
import json
import os
import random
import re
import shutil
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from idna import idnadata  # noqa: E402
from idna.uts46data import uts46_replacements, uts46_starts, uts46_statuses  # noqa: E402

shutil.rmtree("data", ignore_errors=True)
os.makedirs("data")

jobs = []


def job(name, ops):
    jobs.append({"name": name, "ops": ops})


def enc(s, **kw):
    return dict(op="encode", s=s, **kw)


def dec(s, **kw):
    return dict(op="decode", s=s, **kw)


def both(s):
    # What a URL library does: UTS #46 on, then back for display.
    return [enc(s, uts46=True), dec(s, uts46=True)]


SITES = ["Bücher.example", "münchen.de", "MÜNCHEN.DE", "straße.de", "Faß.de", "ﬁle.example", "Ⅷ.example",
         "①②.com", "ＡＢＣ．ｃｏｍ", "example。com", "日本語。ＪＰ", "例え.テスト", "правительство.рф",
         "ПРАВИТЕЛЬСТВО.РФ", "한국.kr", "مثال.إختبار", "דוגמה.טעסט", "ελληνικά.gr", "ΕΛΛΗΝΙΚΆ.GR",
         "ç.com", "ç.com", "việt.vn", "VIỆT.VN", "ไทย.th", "ภาษาไทย.ไทย", "भारत.भारत", "नमस्ते.in",
         "中国.中国", "香港.香港", "españa.es", "ESPAÑA.ES", "øl.no", "æble.dk", "ĳssel.nl", "ǅemal.ba",
         "℡.example", "㎒.example", "ｈｔｔｐｓ．ｅｘａｍｐｌｅ", "soft­hyphen.com", "zero​width.com",
         "각.kr", "Ⓐⓑ.com", "ǆ.com", "ς.gr", "Σ.gr", "ᲊ.ge", "𐵀.example", "xn--bcher-kva.example",
         "xn--mnchen-3ya.de", "xn--zca.de", "xn--80aealotwbjpid2k.xn--p1ai", "xn--3e0b707e.kr",
         "xn--mgbh0fb.xn--kgbechtv", "xn--fsqu00a.xn--0zwm56d", "XN--BCHER-KVA.EXAMPLE", "xn--wgv71a119e.jp",
         "xn--n3h.example", "xn--i-7iq.ws", "xn--ls8h.la"]

job("sites, mapped and back", [x for s in SITES for x in both(s)])

job("strict IDNA 2008", [
    enc("bücher.example"), enc("Bücher.example"), enc("straße.de"), enc("ﬁle.example"), enc("☕.us"),
    enc("i❤.ws"), enc("example。com"), enc("example。com", strict=True), enc("日本語。jp"), enc("ascii.example"),
    enc("ASCII.Example"), enc("a\x00b.com"), enc("under_score.com"), enc("ç.com"),
    dec("xn--bcher-kva.example"), dec("XN--BCHER-KVA.example"), dec("xn--n3h.example"), dec("xn--zca.de"),
    dec("bücher.example"), dec("Bücher.example"), dec("example.com."), dec(b"xn--bcher-kva.example".decode()),
])

job("label rules", [
    enc("-abc.com"), enc("abc-.com"), enc("ab--cd.com"), enc("xn--abc.com"), enc("xn--.com"), enc("xn--abc-.com"),
    dec("xn--.com"), dec("xn--abc-.com"), dec("xn---bbk.com"), dec("xn--bbk.com"), dec("xn--zz.com"),
    dec("xn--99999999999999.com"), dec("xn--a.com"), dec("xn--ab-.com"), dec("xn--ls8h"), dec("xn--ls8h-"),
    dec("xn--Mnchen-3ya.de"), dec("xn--mnchen-3yA.de"), dec("xn--tda"), dec("xn--4ca0bs"),
    enc("́abc.com"), enc("́abc.com", uts46=True), enc("a‍b.com"), enc("क्‍ष.in"),
    enc("ab‌c.com"), enc("ن‌ی.ir"), enc("ب‌a.ir"), enc("col·legi.cat"), enc("a·b.cat"),
    enc("·l.cat"), enc("α͵β.gr"), enc("α͵.gr"), enc("͵β.gr"), enc("א׳.il"), enc("a׳.il"), enc("ア・イ.jp"),
    enc("a・b.jp"), enc("・.jp"), enc("٠١.eg"), enc("٠۱.eg"), enc("۰۱.ir"), enc("͸.com"), enc("\x01.com"),
    enc("\U000e0001.com", uts46=True), enc(".com"),
])

job("bidi", [
    {"op": "bidi", "s": s, "ltr": ltr} for s in ["abc", "aא", "א1", "١א", "אa", "א١1", "א̀", "א-", "abcאd",
                                               "مثال", "مثال1", "مثال١", "à", "1abc", "abc1", "abc-", "ab̀",
                                               "𐵀", "١", "1", "אב١٢", "א ב"]
    for ltr in (False, True)
])

job("uts46 mapping", [
    {"op": "remap", "s": s, "std3": std3}
    for s in ["Example.COM", "under_score.com", "a!b.com", "a！b.com", "ＡＢＣ", "℡", "㎒", "ß", "ẞ", "Ⅻ", "⑴.com",
              "⒈.com", "soft­hyphen", "zero​width", "ﬀ", "Ǆ", "Ꭰ", "İ", "İstanbul", "x́",
              "가", "각", "Å", "Å", "Å", "ȩ́", "ȩ́", "̈́",
              "ｶﾞ", "ｶﾞ", "ﾞ", " ", " ", "a b", "⒈", " ", "a　b", "ᲊ", "𐵀"]
    for std3 in (True, False)
])

job("labels one at a time", [
    {"op": o, "s": s} for o in ("alabel", "ulabel", "check_label")
    for s in ["bücher", "BÜCHER", "xn--bcher-kva", "XN--BCHER-KVA", "abc", "ABC", "", "a" * 63, "a" * 64,
              "ü" * 30, "ü" * 60, "xn--" + "a" * 59, "ç", "ç", "a‍b", "aא", "́a", "a b"]
])

job("domain lengths", [
    enc(".".join(["a" * 63] * 3 + ["a" * 61])), enc(".".join(["a" * 63] * 3 + ["a" * 61]) + "."),
    enc(".".join(["a" * 63] * 3 + ["a" * 62])), enc(".".join(["a" * 63] * 3 + ["a" * 62]) + "."),
    enc(".".join(["ü" * 20] * 6)), enc("ü" * 1025), enc("a" * 1025, uts46=True), dec("a" * 255), dec("a." * 127),
    enc(""), enc("."), enc(".."), enc("a..b"), enc(".a"), dec(""), dec("."), dec("a..b"), enc("a."), dec("a."),
    enc("", uts46=True), enc("。", uts46=True), enc("a。", uts46=True),
])

job("display decoding", [
    dec(s, display=True) for s in ["xn--bcher-kva.example", "xn--zz.example", "XN--ZZ.Example", "xn---bbk.com",
                                   "good.xn--99999999.bad", "xn--a.xn--b.c", "-bad.xn--zz", "xn--n3h.com"]
])

job("incremental", [
    {"op": "inc_encode", "chunks": c} for c in [["bücher", ".exa", "mple"], ["bücher.", "example."], ["日本", "語。", "jp"],
                                                 ["a" * 63 + ".", "a" * 63 + ".", "a" * 63 + ".", "a" * 61 + "."],
                                                 ["a" * 63 + ".", "a" * 63 + ".", "a" * 63 + ".", "a" * 62],
                                                 ["", "ab", "", "c.d"], ["xn--", "abc"], ["-bad.", "good"]]
] + [
    {"op": "inc_decode", "chunks": c} for c in [["xn--bcher", "-kva.exa", "mple"], ["xn--bcher-kva.", "example."],
                                                 ["a" * 200, "a" * 54], ["a" * 200, "a" * 55], ["abc", "dü"],
                                                 ["", "xn--zca", ".de"], ["xn--zz.", "ok"]]
] + [
    {"op": "codec_encode", "s": s} for s in ["bücher.example", "", "bad_label.com", "☕.us"]
] + [
    {"op": "codec_decode", "s": s} for s in ["xn--bcher-kva.example", "", "xn--zz", "dü.de"]
])

job("hosts in URLs", [
    {"op": "host", "s": s} for s in ["example.com", "Bücher.example", "*.example.com", ".example.com", "☕.us",
                                     "münchen.de", "exa_mple.com", "日本語.jp", "a" * 64 + ".com", "xn--zz.com",
                                     "ﬁle.example", "１２３.example", "*ü.com"]
])

job("command line", [
    {"op": "cli", "args": a} for a in [["bücher.example"], ["xn--bcher-kva.example"], ["-e", "xn--bcher-kva.example"],
                                       ["bücher.example", "xn--zca.de", "☕.us"], ["xn--zca.de", "straße.de", "xn--zz"],
                                       ["--strict", "Bücher.example"], ["Bücher.example"], ["-d", "BÜCHER.example"],
                                       ["-d", "--strict", "xn--bcher-kva.example"], ["-e", "-d", "x"], ["--version"],
                                       ["-x"], []]
] + [{"op": "cli", "args": [], "stdin": ["  bücher.example  ", "", "xn--zca.de", "\t", "☕.us"]}])

# Random domains from pieces, and random A-labels.
rnd = random.Random(20261019)
POOL = (list("abcdefghijklmnopqrstuvwxyz0123456789-") + list("ABCXYZ") + list("äöüßéèçñøåæœ") + list("ÄÖÜÉ")
        + list("αβγδΣςπ") + list("абвгдЖЯ") + list("אבגד") + list("ابتث") + list("١٢") + list("日本中文")
        + list("アイウ・") + list("가나다") + list("กขค") + list("कखग्") + ["́", "̈", "̧", "‌",
                                                                        "‍", "­", "ﬁ", "Ⅸ", "①",
                                                                        "ｂ", "．", "。", "_", "!", "☕", "·"])


def rnd_label():
    return "".join(rnd.choice(POOL) for _ in range(rnd.randint(1, 7)))


def rnd_alabel():
    return "xn--" + "".join(rnd.choice("abcdefghijklmnopqrstuvwxyz0123456789-") for _ in range(rnd.randint(1, 10)))


for n in range(12):
    ops = []
    for _ in range(12):
        s = ".".join(rnd_label() for _ in range(rnd.randint(1, 3)))
        k = rnd.random()
        if k < 0.5:
            ops.append(enc(s, uts46=True, std3=rnd.random() < 0.5))
        elif k < 0.7:
            ops.append(enc(s))
        elif k < 0.85:
            ops.append({"op": "remap", "s": s, "std3": rnd.random() < 0.5})
        else:
            ops.append(dec(s, uts46=True))
    for _ in range(6):
        ops.append(dec(rnd_alabel() + "." + rnd.choice(["com", "de", rnd_alabel()]), display=rnd.random() < 0.3))
    job(f"random {n + 1}", ops)

# Encoded names round trip: what the random Unicode labels encode to,
# decoded again.
for n in range(3):
    ops = []
    for _ in range(15):
        s = rnd_label()
        try:
            import idna  # noqa: E402

            a = idna.encode(s, uts46=True).decode()
        except Exception:
            a = rnd_alabel()
        ops.append(dec(a))
    job(f"round trip {n + 1}", ops)

with open("data/jobs.jsonl", "w") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")

# ------------------------------------------------------------ the tables

DOTS = "[.。．｡]"


def row(cp):
    return cp if cp < 256 else bisect.bisect_right(uts46_starts, cp) - 1


covered = set(range(0x80))
strings = []
for j in jobs:
    for op in j["ops"]:
        for k in ("s",):
            if k in op:
                strings.append(op[k])
        for k in ("chunks", "args", "stdin"):
            strings.extend(op.get(k, []))
for s in strings:
    covered.update(ord(c) for c in s)


def punycode_chars(s):
    # The characters an A-label in s decodes to, whether or not the
    # result is valid.
    out = set()
    for label in re.split(DOTS, s):
        b = label.lower()
        if b.startswith("xn--") and b.isascii():
            try:
                out.update(ord(c) for c in b[4:].encode().decode("punycode"))
            except Exception:
                pass
    return out


for s in strings:
    covered |= punycode_chars(s)
    covered |= punycode_chars("".join(uts46_replacements[row(ord(c))] or c for c in s))


def decomp(cp):
    d = unicodedata.decomposition(chr(cp))
    if not d or d.startswith("<"):
        return []
    return [int(x, 16) for x in d.split()]


# Every primary composite whose two halves are covered.
composites = {}
for cp in range(0x110000):
    if 0xD800 <= cp < 0xE000:
        continue
    d = decomp(cp)
    if len(d) == 2 and unicodedata.normalize("NFC", chr(cp)) == chr(cp):
        composites.setdefault(d[0], []).append((d[1], cp))
# Hangul syllables compose by formula, and unicodedata lists no
# decomposition for them.
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
        rep = uts46_replacements[row(cp)]
        if rep:
            more.update(ord(c) for c in rep)
        more.update(decomp(cp))
        for second, comp in composites.get(cp, []):
            if second in covered:
                more.add(comp)
    more -= covered
    if not more:
        break
    covered |= more

with open("data/unicode.txt", "w") as f:
    f.write("# cp;ccc;canonical decomposition;flags (p not printable, n no name, c primary composite);bidi;category\n")
    for cp in sorted(covered):
        ch = chr(cp)
        if 0xD800 <= cp < 0xE000:
            f.write("%x;0;;pn;%s;%s\n" % (cp, unicodedata.bidirectional(ch), unicodedata.category(ch)))
            continue
        d = decomp(cp)
        flags = ("p" if not ch.isprintable() else "") + ("n" if not unicodedata.name(ch, "") else "")
        if len(d) == 2 and unicodedata.normalize("NFC", ch) == ch:
            flags += "c"
        f.write("%x;%d;%s;%s;%s;%s\n" % (cp, unicodedata.combining(ch), " ".join("%x" % x for x in d), flags,
                                         unicodedata.bidirectional(ch), unicodedata.category(ch)))

rows = sorted({row(cp) for cp in covered})
with open("data/uts46.txt", "w") as f:
    f.write("# start;status;replacement\n")
    for i in rows:
        rep = uts46_replacements[i]
        f.write("%x;%s;%s\n" % (uts46_starts[i], chr(uts46_statuses[i]),
                                " ".join("%x" % ord(c) for c in rep) if rep else ""))


def ranges(name, rs):
    return ["%s %x %x" % (name, r >> 32, r & 0xFFFFFFFF) for r in rs]


with open("data/idnadata.txt", "w") as f:
    f.write("# set start end (end exclusive)\n")
    for k, v in idnadata.codepoint_classes.items():
        f.write("\n".join(ranges(k, v)) + "\n")
    for k, v in idnadata.scripts.items():
        f.write("\n".join(ranges("script:" + k, v)) + "\n")
    for k, v in idnadata.joining_types.items():
        f.write("\n".join(ranges("joining:" + k, v)) + "\n")

print(len(jobs), "jobs,", sum(len(j["ops"]) for j in jobs), "operations,", len(covered), "characters,",
      len(rows), "UTS #46 rows")
