# The NFKD decompositions mini_jellyfish.kara carries, from Python's
# unicodedata: every character in BLOCKS that NFKD changes. Run as a
# script, it prints them as the Kara function nfkd_table(); mk.py checks
# that NFKD of every string in data/ is these decompositions joined.
import unicodedata

BLOCKS = [
    (0x00A0, 0x052F),  # Latin-1 to Latin Extended-B, IPA, Greek, Cyrillic
    (0x1E00, 0x1FFF),  # Latin Extended Additional, Greek Extended
    (0x2000, 0x218F),  # punctuation, letterlike symbols, number forms
    (0xFB00, 0xFB4F),  # alphabetic presentation forms (ligatures)
    (0xFF00, 0xFFEF),  # halfwidth and fullwidth forms
]


def table():
    out = []
    for lo, hi in BLOCKS:
        for o in range(lo, hi + 1):
            c = chr(o)
            d = unicodedata.normalize("NFKD", c)
            if d != c:
                out.append((c, d))
    return out


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
