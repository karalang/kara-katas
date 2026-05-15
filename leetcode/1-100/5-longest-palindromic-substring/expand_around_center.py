"""LeetCode #5: Longest Palindromic Substring — expand around center.
O(n²) time, O(n) extra space for the indexed char list.

Algorithmic mirror of expand_around_center.kara. Output format matches
line-for-line so the two can be diffed directly.
"""

from __future__ import annotations


def expand(chars: list[str], lo0: int, hi0: int) -> tuple[int, int]:
    # Returns (start, length) of the palindrome centered between lo0 and hi0.
    # Loop invariant matches the Kāra version: on exit, the matched range is
    # chars[lo+1 .. hi-1] inclusive, so start = lo + 1 and length = hi - lo - 1.
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


def report(s: str) -> None:
    start, length = longest_palindrome(s)
    print(start)
    print(length)


def main() -> None:
    report("babad")             # expect: 0 3   ("bab")
    report("cbbd")              # expect: 1 2   ("bb")
    report("a")                 # expect: 0 1
    report("ac")                # expect: 0 1
    report("")                  # expect: 0 0
    report("racecar")           # expect: 0 7
    report("abacdfgdcaba")      # expect: 0 3   ("aba")
    report("ababababa")         # expect: 0 9
    report("forgeeksskeegfor")  # expect: 3 10  ("geeksskeeg")
    report("aaa")               # expect: 0 3


if __name__ == "__main__":
    main()
