"""Benchmark workload — expand-around-center O(n²) Longest Palindromic
Substring.

Algorithmic mirror of bench/expand_around_center.kara. See ../README.md
§ Benchmarks for the input shape and K choice.
"""

from __future__ import annotations


def expand(chars: list[str], lo0: int, hi0: int) -> tuple[int, int]:
    lo, hi = lo0, hi0
    n = len(chars)
    while lo >= 0 and hi < n and chars[lo] == chars[hi]:
        lo -= 1
        hi += 1
    return (lo + 1, hi - lo - 1)


def longest_palindrome(s: str) -> tuple[int, int]:
    chars = list(s)
    n = len(chars)
    best_start = 0
    best_len = 0
    for i in range(n):
        start, length = expand(chars, i, i)
        if length > best_len:
            best_start, best_len = start, length
        start, length = expand(chars, i, i + 1)
        if length > best_len:
            best_start, best_len = start, length
    return (best_start, best_len)


def main() -> None:
    data = "a" * 5000

    sum_result = 0
    for _ in range(10):
        start, length = longest_palindrome(data)
        sum_result += start + length
    print(sum_result)


if __name__ == "__main__":
    main()
