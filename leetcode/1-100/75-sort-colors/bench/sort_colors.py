"""Benchmark workload — Sort Colors (LeetCode #75).

Python mirror of bench/sort_colors.kara. Same Dutch National Flag one-pass sort
over a list allocated once and refilled in place. Runs K=20,000 iterations — 1/10
of the compiled mirrors' K=200,000 — because a pure-Python sort loop at full scale
is ~150 s; this row is timed separately and its sink is NOT cross-checked against
the compiled sink (different K). The kata's correctness is verified by the
top-level sort_colors.py oracle instead.
"""

from __future__ import annotations


def sort_colors(a: list[int]) -> None:
    n = len(a)
    if n == 0:
        return
    low, mid, high = 0, 0, n - 1
    while mid <= high:
        if a[mid] == 0:
            a[low], a[mid] = a[mid], a[low]
            low += 1
            mid += 1
        elif a[mid] == 1:
            mid += 1
        else:
            a[mid], a[high] = a[high], a[mid]
            high -= 1


def main() -> None:
    n = 500
    total = 20_000  # 1/10 of the compiled mirrors' K; timed-only, not cross-checked
    modulus = 1_000_000_007

    a = [0] * n

    acc = 0
    for k in range(total):
        for j in range(n):
            a[j] = (j * 7 + k * 13) % 3
        sort_colors(a)
        for j in range(n):
            acc = (acc * 131 + a[j]) % modulus
    print(acc)


if __name__ == "__main__":
    main()
