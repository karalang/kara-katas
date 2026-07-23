"""Benchmark workload for LeetCode #214 — Shortest Palindrome (Python; scale lane)."""


def prefix_lps(base, w, width, comb, fail):
    m = 2 * width + 1
    for i in range(width):
        comb[i] = base[w + i]
    comb[width] = -1
    for i in range(width):
        comb[width + 1 + i] = base[w + width - 1 - i]

    fail[0] = 0
    length = 0
    idx = 1
    while idx < m:
        if comb[idx] == comb[length]:
            length += 1
            fail[idx] = length
            idx += 1
        elif length > 0:
            length = fail[length - 1]
        else:
            fail[idx] = 0
            idx += 1
    return fail[m - 1]


def main():
    big = 260000
    width = 512
    alpha = 2

    base = []
    state = 12345
    for _ in range(big):
        state = (state * 1103515245 + 12345) & 2147483647
        base.append(state % alpha)

    m = 2 * width + 1
    comb = [0] * m
    fail = [0] * m

    windows = big - width
    sink = 0
    for w in range(windows):
        sink += prefix_lps(base, w, width, comb, fail)
    print(sink)


main()
