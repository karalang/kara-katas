"""LeetCode 266 — Palindrome Permutation (Python mirror / oracle).

Mirrors palindrome_permutation.kara algorithm-for-algorithm: a byte histogram,
then count how many entries are odd. At most one, not exactly one.
"""


def can_permute_palindrome(s):
    counts = [0] * 256
    for b in s.encode():
        counts[b] += 1
    odd = sum(1 for c in counts if c % 2 == 1)
    return odd <= 1


def report(s):
    print(f'"{s}" -> {"true" if can_permute_palindrome(s) else "false"}')


def main():
    for s in ("code", "aab", "carerac", "", "a", "aa", "ab", "aabb", "aabbcc",
              "aaabbb", "aaabbbb", "zzzzzzzz", "abcabcabc", "abcabcabcd"):
        report(s)


main()
