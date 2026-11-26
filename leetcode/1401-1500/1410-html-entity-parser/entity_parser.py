# LeetCode #1410, Python mirror of entity_parser.kara: one walk, at each
# `&` the name up to the next `;` within seven characters looked up.

ENTITIES = {"&quot;": "\"", "&apos;": "'", "&amp;": "&", "&gt;": ">", "&lt;": "<", "&frasl;": "/"}


def entity_parser(text):
    out = []
    i = 0
    while i < len(text):
        if text[i] == "&":
            window = text[i:min(i + 7, len(text))]
            end = window.find(";")
            if end >= 0 and window[:end + 1] in ENTITIES:
                out.append(ENTITIES[window[:end + 1]])
                i += end + 1
                continue
        out.append(text[i])
        i += 1
    return "".join(out)


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


PIECES = ["a", "b", " ", "&", ";", "&quot;", "&apos;", "&amp;", "&gt;", "&lt;", "&frasl;", "&amp", "&gt", "&quot",
          "&ambassador;", "&lt;;", "&&", "amp;", "&frasl"]


def drawn(n):
    return "".join(PIECES[next_random() % len(PIECES)] for _ in range(n))


def checksum(check, s):
    for b in s.encode():
        check = (check * 131 + b) % 1000000007
    return check


def main():
    global seed
    print(entity_parser("&amp; is an HTML entity but &ambassador; is not."))
    print(entity_parser("and I quote: &quot;...&quot;"))
    print(" | ".join(entity_parser(t) for t in
                     ["&amp;gt;", "&&gt;", "x &frasl; y &lt;&gt; &apos;z&apos;", "&quot&quot;;", "&"]))
    seed = 1410
    nested = "&amp;gt;" * 12500
    big = entity_parser(drawn(20000))
    print(f"10^5 characters, 20000 pieces: {len(entity_parser(nested))} {len(big)} {checksum(0, big)}")
    check = 0
    total = 0
    for _ in range(2000):
        n = 1 + next_random() % 30
        out = entity_parser(drawn(n))
        total += len(out)
        check = checksum(check, out)
    print(f"2000 random texts: {total} characters, checksum {check}")


main()
