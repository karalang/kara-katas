"""LeetCode #3: Longest Substring Without Repeating Characters — sliding window
with a last-index map. O(n) time, O(min(n, alphabet)) space.

Algorithmic mirror of sliding_window.kara. Output format matches line-for-line
so the two can be diffed directly.
"""

from __future__ import annotations


def length_of_longest_substring(s: str) -> int:
    # Maintain a half-open window [left, right). For each character, if we've
    # seen it before at an index inside the current window, jump `left` to
    # one past that index — each duplicate is removed by a single pointer
    # jump, never by a shrink loop.
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


def report(s: str) -> None:
    print(length_of_longest_substring(s))


def main() -> None:
    report("abcabcbb")    # expect: 3   ("abc")
    report("bbbbb")       # expect: 1   ("b")
    report("pwwkew")      # expect: 3   ("wke")
    report("")            # expect: 0
    report(" ")           # expect: 1
    report("au")          # expect: 2
    report("dvdf")        # expect: 3   ("vdf")
    report("tmmzuxt")     # expect: 5   ("mzuxt")


if __name__ == "__main__":
    main()
