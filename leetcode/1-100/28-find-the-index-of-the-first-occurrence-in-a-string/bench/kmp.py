"""Benchmark workload — KMP strStr, same adversarial input as brute_force.py.

Algorithmic mirror of bench/kmp.kara. See ../README.md § Benchmarks.
"""

from __future__ import annotations


def build_lps(pat: bytes, m: int) -> list[int]:
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if pat[i] == pat[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length > 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps


def str_str(haystack: bytes, needle: bytes) -> int:
    hn = len(haystack)
    nn = len(needle)
    if nn == 0:
        return 0
    if nn > hn:
        return -1
    lps = build_lps(needle, nn)
    i = 0
    j = 0
    while i < hn:
        if haystack[i] == needle[j]:
            i += 1
            j += 1
            if j == nn:
                return i - nn
        elif j > 0:
            j = lps[j - 1]
        else:
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
    for _ in range(100):
        total += str_str(haystack, needle)
    print(total)


if __name__ == "__main__":
    main()
