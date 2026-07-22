"""LeetCode 159 — Longest Substring with At Most Two Distinct Characters.

Sliding window: grow right, shrink left whenever the window holds more than two
distinct chars, tracking per-char counts in a dict. Mirrors the Kāra version.
Premium.
"""


def longest(s):
    counts = {}
    left = 0
    best = 0
    for right in range(len(s)):
        c = s[right]
        counts[c] = counts.get(c, 0) + 1
        while len(counts) > 2:
            lc = s[left]
            if counts[lc] <= 1:
                del counts[lc]
            else:
                counts[lc] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


def main():
    print(longest("eceba"))       # 3
    print(longest("ccaabbb"))     # 5
    print(longest("a"))           # 1
    print(longest("ab"))          # 2
    print(longest("abaccc"))      # 4
    print(longest(""))            # 0
    print(longest("aaaaaa"))      # 6
    print(longest("abcabcabc"))   # 2


main()
