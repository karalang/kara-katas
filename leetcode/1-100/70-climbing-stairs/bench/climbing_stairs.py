"""Benchmark workload — Climbing Stairs (LeetCode #70).

Python mirror of bench/climbing_stairs.kara. The ★'s two-counter Fibonacci
recurrence over a sweep of n = 1 + k%45, folding each result into the same
rolling polynomial hash. CPython is multi-second at the compiled mirrors'
K=30_000_000, so this runs K=3_000_000 (1/10th) — timed separately and NOT
cross-checked against the compiled sink. See ../README.md § Benchmarks.
"""

from __future__ import annotations


def climb(n: int) -> int:
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


def main() -> None:
    total = 3_000_000
    modulus = 1_000_000_007
    span = 45

    acc = 0
    for k in range(total):
        n = 1 + (k % span)
        acc = (acc * 131 + climb(n)) % modulus
    print(acc)


if __name__ == "__main__":
    main()
