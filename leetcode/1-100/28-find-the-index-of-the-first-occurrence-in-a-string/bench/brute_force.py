"""Benchmark workload — brute-force sliding-window strStr.

Algorithmic mirror of bench/brute_force.kara. See ../README.md § Benchmarks for
the adversarial-input choice and the N, M, K values.
"""

from __future__ import annotations


def str_str(haystack: bytes, needle: bytes) -> int:
    hn = len(haystack)
    nn = len(needle)
    if nn == 0:
        return 0
    if nn > hn:
        return -1
    i = 0
    while i <= hn - nn:
        j = 0
        while j < nn and haystack[i + j] == needle[j]:
            j += 1
        if j == nn:
            return i
        i += 1
    return -1


def main() -> None:
    n = 2_000_000
    m = 16
    haystack = bytearray(b"a" * n)
    haystack[n - 1] = ord("b")
    needle = bytearray(b"a" * m)
    needle[m - 1] = ord("b")

    total = 0
    for _ in range(10):
        total += str_str(haystack, needle)
    print(total)


if __name__ == "__main__":
    main()
