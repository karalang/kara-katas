"""Benchmark workload — Sqrt(x) (LeetCode #69).

Python mirror of bench/sqrtx.kara. The ★'s binary search for floor(sqrt(x)) run
over a Knuth-multiplicative sweep of x across [0, 2^31), folding results into the
same rolling polynomial hash. CPython is multi-second at the compiled mirrors'
K=3_000_000, so this runs K=300_000 (1/10th) — timed separately and NOT
cross-checked against the compiled sink. See ../README.md § Benchmarks.
"""

from __future__ import annotations


def my_sqrt(x: int) -> int:
    lo, hi, ans = 0, x, 0
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if mid * mid <= x:
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return ans


def main() -> None:
    total = 300_000
    modulus = 1_000_000_007
    rng = 2_147_483_648  # 2^31

    acc = 0
    for k in range(total):
        x = (k * 2_654_435_761) % rng
        acc = (acc * 131 + my_sqrt(x)) % modulus
    print(acc)


if __name__ == "__main__":
    main()
