# The NFKD data mini_mnemonic.kara carries, from Python's unicodedata:
# the decomposition of every character in BLOCKS that NFKD changes, and
# the combining class of every combining mark in MARKS. Hangul syllables
# decompose by the Unicode algorithm, so they need no table. Run as a
# script, it prints the Kara functions nfkd_table() and ccc_table();
# mk.py checks that nfkd() below gives Python's NFKD for every string in
# data/, wordlists included.
import unicodedata

BLOCKS = [
    (0x00A0, 0x024F),  # Latin-1 to Latin Extended-B
    (0x0400, 0x04FF),  # Cyrillic
    (0x1E00, 0x1EFF),  # Latin Extended Additional
    (0x2000, 0x218F),  # punctuation, super- and subscripts, number forms
    (0x3000, 0x30FF),  # CJK punctuation, hiragana, katakana
    (0xFF00, 0xFFEF),  # halfwidth and fullwidth forms
]
MARKS = [(0x0300, 0x036F), (0x0483, 0x0489), (0x3099, 0x309A)]


def table():
    out = []
    for lo, hi in BLOCKS:
        for o in range(lo, hi + 1):
            c = chr(o)
            d = unicodedata.normalize("NFKD", c)
            if d != c:
                out.append((c, d))
    return out


def classes():
    out = []
    for lo, hi in MARKS:
        for o in range(lo, hi + 1):
            k = unicodedata.combining(chr(o))
            if k:
                out.append((chr(o), k))
    return out


DECOMP = dict(table())
CCC = dict(classes())


def hangul(c):
    s = ord(c) - 0xAC00
    if not 0 <= s < 11172:
        return None
    lead, vowel, tail = 0x1100 + s // 588, 0x1161 + (s % 588) // 28, s % 28
    return chr(lead) + chr(vowel) + (chr(0x11A7 + tail) if tail else "")


def nfkd(s):
    chars = []
    for c in s:
        h = hangul(c)
        chars.extend(h if h else DECOMP.get(c, c))
    # canonical ordering: each run of marks sorted, stably, by class
    i = 0
    while i < len(chars):
        if CCC.get(chars[i], 0) == 0:
            i += 1
            continue
        j = i
        while j < len(chars) and CCC.get(chars[j], 0) != 0:
            j += 1
        chars[i:j] = sorted(chars[i:j], key=lambda c: CCC[c])
        i = j
    return "".join(chars)


def kara_lit(s):
    return "".join(ch if 0x20 <= ord(ch) < 0x7f and ch not in "\\\"'" else "\\u{%x}" % ord(ch) for ch in s)


if __name__ == "__main__":
    rows = table()
    chunks = [rows[i:i + 150] for i in range(0, len(rows), 150)]
    print("// NFKD for the characters of tables.py's BLOCKS that it changes,")
    print("// from Python's unicodedata.")
    print("fn nfkd_table() -> Map[char, String] {")
    print("    let mut m: Map[char, String] = Map.new();")
    for k in range(len(chunks)):
        print("    nfkd_part_%d(mut m);" % k)
    print("    m")
    print("}")
    for k, chunk in enumerate(chunks):
        print()
        print("fn nfkd_part_%d(m: mut ref Map[char, String]) {" % k)
        for c, d in chunk:
            print("    m.insert('%s', \"%s\".to_string());" % (kara_lit(c), kara_lit(d)))
        print("}")
    print()
    print("// The combining class of each mark in tables.py's MARKS.")
    print("fn ccc_table() -> Map[char, i64] {")
    print("    let mut m: Map[char, i64] = Map.new();")
    for c, k in classes():
        print("    m.insert('%s', %d);" % (kara_lit(c), k))
    print("    m")
    print("}")
