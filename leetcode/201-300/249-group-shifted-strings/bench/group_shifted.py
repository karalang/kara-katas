"""Benchmark workload for LeetCode #249 — Group Shifted Strings (Python; scale lane)."""


def canonical(word):
    b = word.encode()
    n = len(b)
    if n == 0:
        return ""
    shift = b[0] - ord('a')
    out = []
    for i in range(n):
        c = ((b[i] - ord('a') - shift) + 26) % 26
        out.append(f"{c},")
    return "".join(out)


def main():
    words_n = 120000
    rounds = 5

    words = []
    state = 249249
    for _ in range(words_n):
        state = (state * 1103515245 + 12345) & 2147483647
        ln = (state // 65536) % 10 + 3
        state = (state * 1103515245 + 12345) & 2147483647
        seed = (state // 65536) % 40
        state = (state * 1103515245 + 12345) & 2147483647
        shift = (state // 65536) % 26

        s = []
        for i in range(ln):
            base = (seed * 7 + i * 11) % 26
            ch = (base + shift) % 26
            s.append(chr(97 + ch))
        words.append("".join(s))

    sink = 0
    for _ in range(rounds):
        table = {}
        groups = 0
        keysum = 0
        for w in words:
            key = canonical(w)
            for c in key.encode():
                keysum = (keysum * 31 + c) % 1000000007
            if key not in table:
                groups += 1
            table.setdefault(key, []).append(w)
        sink = (sink * 131 + groups) % 1000000007
        sink = (sink * 31 + keysum) % 1000000007
    print(sink)


main()
