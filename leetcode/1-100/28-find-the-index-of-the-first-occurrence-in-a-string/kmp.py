"""LeetCode #28: Find the Index of the First Occurrence in a String —
Knuth-Morris-Pratt (KMP).

Algorithmic mirror of kmp.kara. Output format matches line-for-line so the two
can be diffed directly.
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


def str_str(haystack: str, needle: str) -> int:
    h = haystack.encode()
    nee = needle.encode()
    hn = len(h)
    nn = len(nee)
    if nn == 0:
        return 0
    if nn > hn:
        return -1
    lps = build_lps(nee, nn)
    i = 0
    j = 0
    while i < hn:
        if h[i] == nee[j]:
            i += 1
            j += 1
            if j == nn:
                return i - nn
        elif j > 0:
            j = lps[j - 1]
        else:
            i += 1
    return -1


def report(haystack: str, needle: str) -> None:
    r = str_str(haystack, needle)
    print(f"{haystack} ~ {needle}: {r}")


def main() -> None:
    report("sadbutsad", "sad")        # expect: 0
    report("leetcode", "leeto")       # expect: -1
    report("hello", "ll")             # expect: 2
    report("a", "a")                  # expect: 0
    report("", "")                    # expect: 0
    report("abc", "")                 # expect: 0
    report("aaa", "aaaa")             # expect: -1
    report("mississippi", "issip")    # expect: 4
    report("abababcabab", "ababc")    # expect: 4
    report("aaaaab", "aab")           # expect: 3
    report("abc", "abc")              # expect: 0
    report("abc", "c")                # expect: 2


if __name__ == "__main__":
    main()
