# LeetCode #1410 bench, Python: the same walk, at each `&` the name up to the
# next `;` within seven characters looked up, workload and checksum as
# entity_parser.kara.

ENTITIES = {"&quot;": "\"", "&apos;": "'", "&amp;": "&", "&gt;": ">", "&lt;": "<", "&frasl;": "/"}


def entity_parser(text):
    out = []
    i = 0
    n = len(text)
    while i < n:
        if text[i] == "&":
            window = text[i:min(i + 7, n)]
            end = window.find(";")
            if end >= 0:
                symbol = ENTITIES.get(window[:end + 1])
                if symbol is not None:
                    out.append(symbol)
                    i += end + 1
                    continue
        out.append(text[i])
        i += 1
    return "".join(out)


def main():
    pieces = ["a", "b", " ", "&", ";", "&quot;", "&apos;", "&amp;", "&gt;", "&lt;", "&frasl;", "&amp", "&gt", "&quot",
              "&ambassador;", "&lt;;", "&&", "amp;", "&frasl"]
    seed = 1410
    parts = []
    plen = 0
    while plen < 300000:
        seed = (seed * 1103515245 + 12345) % 2147483648
        p = pieces[seed // 65536 % len(pieces)]
        parts.append(p)
        plen += len(p)
    pool = "".join(parts)
    check = 0
    for _ in range(300):
        seed = (seed * 1103515245 + 12345) % 2147483648
        start = seed // 65536 % (len(pool) - 100000)
        out = entity_parser(pool[start:start + 100000])
        check = (check * 131 + len(out) + sum(out.encode())) % 1000000007
    print(f"300 windows of 10^5 characters: checksum {check}")


main()
