"""Benchmark workload — sliding-window O(n) Longest Substring Without
Repeating Characters.

Algorithmic mirror of bench/sliding_window.kara. See ../README.md § Benchmarks
for the input shape and K choice.
"""

from __future__ import annotations


def length_of_longest_substring(s: str) -> int:
    last_idx: dict[str, int] = {}
    left = 0
    best = 0
    for right, c in enumerate(s):
        prev = last_idx.get(c)
        if prev is not None and prev >= left:
            left = prev + 1
        last_idx[c] = right
        window = right - left + 1
        if window > best:
            best = window
    return best


def main() -> None:
    data = "abcdefghijklmnopqrstuvwxyz" * 4000  # 104_000 chars

    sum_result = 0
    for _ in range(20):
        sum_result += length_of_longest_substring(data)
    print(sum_result)


if __name__ == "__main__":
    main()
