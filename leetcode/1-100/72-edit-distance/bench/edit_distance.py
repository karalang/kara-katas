"""Benchmark workload — Edit Distance (LeetCode #72).

Python mirror of bench/edit_distance.kara. Faithful to the kata's Vec-based DP:
each DP row and input string is a list built by `append` (grows), matching Kāra's
`Vec.new()+push` — so the comparison measures the same growing-dynamic-array
discipline. Rolling O(n)-space Levenshtein. CPython is multi-second at the
compiled mirrors' K=400_000, so this runs K=40_000 (1/10th) — timed separately
and NOT cross-checked against the compiled sink. See ../README.md § Benchmarks.
"""

from __future__ import annotations

L = 24


def edit_distance(a: list[int], b: list[int], m: int, n: int) -> int:
    prev: list[int] = []
    for j in range(n + 1):
        prev.append(j)
    for i in range(1, m + 1):
        cur = [i]
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                cur.append(prev[j - 1])
            else:
                x = prev[j - 1]
                if prev[j] < x:
                    x = prev[j]
                if cur[j - 1] < x:
                    x = cur[j - 1]
                cur.append(1 + x)
        prev = cur
    return prev[n]


def main() -> None:
    total = 40_000
    modulus = 1_000_000_007

    acc = 0
    for k in range(total):
        a: list[int] = []
        b: list[int] = []
        for p in range(L):
            a.append((p * 7 + k) % 4)
            b.append((p * 5 + 2 * k) % 4)
        acc = (acc * 131 + edit_distance(a, b, L, L)) % modulus
    print(acc)


if __name__ == "__main__":
    main()
