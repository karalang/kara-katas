"""Benchmark harness for LeetCode #132 — Palindrome Partitioning II.

Mirrors min_cut.kara algorithm-for-algorithm, including the nested
list-of-lists palindrome table. Committed as the correctness oracle; not a
measured lane.
"""

N = 500
ITERS = 400


def min_cut(s):
    b = s.encode()
    n = len(b)
    if n <= 1:
        return 0

    pal = []
    for i in range(n):
        pal.append([i == j for j in range(n)])

    for length in range(2, n + 1):
        for lo in range(0, n - length + 1):
            hi = lo + length - 1
            ends_match = b[lo] == b[hi]
            inner_ok = length == 2 or pal[lo + 1][hi - 1]
            if ends_match and inner_ok:
                pal[lo][hi] = True

    cut = [0] * n
    for i in range(n):
        if pal[0][i]:
            cut[i] = 0
        else:
            best = i
            for j in range(1, i + 1):
                if pal[j][i] and (cut[j - 1] + 1) < best:
                    best = cut[j - 1] + 1
            cut[i] = best
    return cut[n - 1]


def lcg_str(seed, n, alpha):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    out = []
    x = seed
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        target = (x // 65536) % alpha
        for idx, ch in enumerate(alphabet):
            if idx == target:
                out.append(ch)
    return "".join(out)


def main():
    cases = [
        lcg_str(1, N, 2),
        lcg_str(2, N, 4),
        lcg_str(3, N, 26),
        lcg_str(4, N, 3),
    ]
    np_ = len(cases)

    sink = 0
    for it in range(ITERS):
        idx = (it * 3) % np_
        sink = (sink + min_cut(cases[idx])) % 1000000007
    print(sink)


if __name__ == "__main__":
    main()
