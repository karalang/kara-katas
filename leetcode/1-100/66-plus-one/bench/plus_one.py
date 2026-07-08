"""Benchmark workload — Plus One (LeetCode #66).

Python mirror of bench/plus_one.kara. A fixed-width (W=9) decimal digit buffer
driven as a base-10 counter: the ★'s reverse-scan carry applied in place, folding
a rotating digit into the same rolling polynomial-hash sink. CPython is
multi-second at the compiled mirrors' K=80_000_000, so this runs K=8_000_000
(1/10th) — timed separately and NOT cross-checked against the compiled sink.
See ../README.md § Benchmarks.
"""

from __future__ import annotations


def main() -> None:
    total = 8_000_000
    modulus = 1_000_000_007
    W = 9

    digits = [0] * W

    acc = 0
    for k in range(total):
        i = W - 1
        while i >= 0:
            if digits[i] < 9:
                digits[i] += 1
                break  # carry absorbed
            digits[i] = 0
            i -= 1
        acc = (acc * 131 + digits[k % W]) % modulus
    print(acc)


if __name__ == "__main__":
    main()
