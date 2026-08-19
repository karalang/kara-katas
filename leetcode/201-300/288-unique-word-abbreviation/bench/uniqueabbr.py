"""Benchmark twin for LeetCode #288 — same algorithm as uniqueabbr.kara."""

CONFLICTED = object()
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def main() -> None:
    dict_n, pool_n, punches = 3_000, 20_000, 1_000_000
    seed = 12345

    def nxt(s):
        return (s * 1103515245 + 12345) & 2147483647

    words = []
    for _ in range(dict_n):
        seed = nxt(seed)
        n = 3 + ((seed // 65536) % 8)
        cs = []
        for _ in range(n):
            seed = nxt(seed)
            cs.append(LETTERS[(seed // 65536) % 26])
        words.append("".join(cs))

    idx = {}
    for w in words:
        a = w if len(w) <= 2 else f"{w[0]}{len(w) - 2}{w[-1]}"
        prev = idx.get(a)
        if prev is None:
            idx[a] = w
        elif prev is not CONFLICTED and prev != w:
            idx[a] = CONFLICTED

    pool = []
    for i in range(pool_n):
        if i % 2 == 0:
            pool.append(words[(i * 7) % dict_n])
        else:
            seed = nxt(seed)
            n = 3 + ((seed // 65536) % 8)
            cs = []
            for _ in range(n):
                seed = nxt(seed)
                cs.append(LETTERS[(seed // 65536) % 26])
            pool.append("".join(cs))

    unique_count = 0
    for i in range(punches):
        word = pool[i % pool_n]
        a = word if len(word) <= 2 else f"{word[0]}{len(word) - 2}{word[-1]}"
        hit = idx.get(a)
        if hit is None or (hit is not CONFLICTED and hit == word):
            unique_count += 1
    print(f"unique {unique_count}")


if __name__ == "__main__":
    main()
