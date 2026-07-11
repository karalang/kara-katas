"""LeetCode #87: Scramble String — recursive split with char-count pruning.

Mirror of scramble_string.kara. Recurse over index windows of two byte strings: an
identical window is a scramble (early true), windows with different letter multisets
can never match (early false), and the survivors fan out over every split point, each
tried with and without the swap. Same fifteen cases and output shape (an `s1 ~ s2: t/f`
line per case, then a `sink:` fold of the boolean outcomes) so the files diff
line-for-line.
"""

from __future__ import annotations


def scramble(s1: list[int], i1: int, s2: list[int], i2: int, length: int) -> bool:
    equal = True
    for k in range(length):
        if s1[i1 + k] != s2[i2 + k]:
            equal = False
            break
    if equal:
        return True

    counts = [0] * 26
    for k in range(length):
        counts[s1[i1 + k] - 97] += 1
        counts[s2[i2 + k] - 97] -= 1
    for c in range(26):
        if counts[c] != 0:
            return False

    for split in range(1, length):
        if (scramble(s1, i1, s2, i2, split)
                and scramble(s1, i1 + split, s2, i2 + split, length - split)):
            return True
        if (scramble(s1, i1, s2, i2 + length - split, split)
                and scramble(s1, i1 + split, s2, i2, length - split)):
            return True
    return False


def to_vec(s: str) -> list[int]:
    return list(s.encode())


def report(s1: str, s2: str, acc: list[int]) -> None:
    a = to_vec(s1)
    b = to_vec(s2)
    n = len(a)
    found = scramble(a, 0, b, 0, n) if len(b) == n else False
    print(f"{s1} ~ {s2}: {'true' if found else 'false'}")
    bit = 1 if found else 0
    acc[0] = (acc[0] * 131 + bit + 1) % 1000000007


def main() -> None:
    acc = [0]
    report("great", "rgeat", acc)
    report("abcde", "caebd", acc)
    report("a", "a", acc)
    report("", "", acc)
    report("ab", "ba", acc)
    report("ab", "ab", acc)
    report("abc", "bca", acc)
    report("abcd", "badc", acc)
    report("abcd", "cdab", acc)
    report("aabb", "bbaa", acc)
    report("abcd", "acbd", acc)
    report("abcde", "edcba", acc)
    report("abc", "abd", acc)
    report("greatabc", "rgeatabc", acc)
    print(f"sink: {acc[0]}")


if __name__ == "__main__":
    main()
