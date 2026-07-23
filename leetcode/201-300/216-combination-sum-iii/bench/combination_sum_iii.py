"""Benchmark workload for LeetCode #216 — Combination Sum III (Python; scale lane)."""


def count_combos(start, k, remaining, d_pool):
    if k == 0:
        return 1 if remaining == 0 else 0
    total = 0
    d = start
    while d <= d_pool:
        if d > remaining:
            return total
        total += count_combos(d + 1, k - 1, remaining - d, d_pool)
        d += 1
    return total


def main():
    d_pool = 36
    kmax = 6
    nmax = 150

    sink = 0
    for k in range(1, kmax + 1):
        for n in range(1, nmax + 1):
            sink += count_combos(1, k, n, d_pool)
    print(sink)


main()
