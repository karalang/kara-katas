"""Benchmark workload — Sort Colors (LeetCode #75), seq lane (scaled).

Python single-threaded mirror of bench/sort_colors.kara. Same batch of independent
Dutch National Flag sorts of n=59999 {0,1,2} arrays (grown by append), each hashed
and summed. Runs K=200 iterations — 1/10 of the compiled mirrors' K=2000 — because
a pure-Python sort of 60k elements is slow; this row is timed separately and its
sink is NOT cross-checked against the compiled sink (different K). The kata's
correctness is verified by the top-level sort_colors.py oracle instead.
"""

from __future__ import annotations

N = 59999


def sort_and_hash(seed: int) -> int:
    a: list[int] = []
    for j in range(N):
        a.append((j * 7 + seed) % 3)

    low, mid, high = 0, 0, N - 1
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

    acc = 0
    for j in range(N):
        acc = (acc * 131 + a[j]) % 1_000_000_007
    return acc


def main() -> None:
    total = 200  # 1/10 of the compiled mirrors' K; timed-only, not cross-checked
    total_sum = 0
    for i in range(total):
        total_sum += sort_and_hash(i)
    print(total_sum)


if __name__ == "__main__":
    main()
