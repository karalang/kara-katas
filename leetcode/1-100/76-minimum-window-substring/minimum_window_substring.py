"""LeetCode #76: Minimum Window Substring — sliding window with need/have counts.

Mirror of minimum_window_substring.kara. Two pointers over s: grow the right edge
until the window contains all of t (with multiplicity), then shrink the left edge
while it stays complete, recording the shortest complete window. Character counts
live in length-128 tables (ASCII English letters). Like kata #5 we report the
window's (start, length) rather than the substring, plus a hash of the window's
bytes so the content is cross-checked. Same twelve cases and output shape (one
`min_window(...) = start len [hash]` per line, then a `sums:` fold) so the files
diff line-for-line.
"""

from __future__ import annotations


def min_window(s: str, t: str) -> tuple[int, int]:
    sb = s.encode()
    tb = t.encode()
    n, m = len(s), len(t)
    if m > n:
        return (-1, 0)

    need = [0] * 128
    required = 0
    for i in range(m):
        c = tb[i]
        if need[c] == 0:
            required += 1
        need[c] += 1

    have = [0] * 128
    formed = 0
    l = 0
    best_start, best_len = -1, 0

    for r in range(n):
        cr = sb[r]
        have[cr] += 1
        if have[cr] == need[cr]:
            formed += 1
        while formed == required:
            win = r - l + 1
            if best_start == -1 or win < best_len:
                best_start, best_len = l, win
            cl = sb[l]
            have[cl] -= 1
            if have[cl] < need[cl]:
                formed -= 1
            l += 1

    return (best_start, best_len)


def window_hash(s: str, start: int, length: int) -> int:
    if start < 0:
        return 0
    sb = s.encode()
    acc = 0
    for i in range(length):
        acc = (acc * 131 + sb[start + i]) % 1000000007
    return acc


def report(s: str, t: str, acc: list[str]) -> None:
    start, length = min_window(s, t)
    h = window_hash(s, start, length)
    print(f'min_window("{s}","{t}") = {start} {length} [{h}]')
    acc.append(f"{start}:{length}:{h}")


def main() -> None:
    acc: list[str] = []
    report("ADOBECODEBANC", "ABC", acc)
    report("a", "a", acc)
    report("a", "aa", acc)
    report("a", "b", acc)
    report("ab", "b", acc)
    report("ab", "a", acc)
    report("aa", "aa", acc)
    report("cabwefgewcwaefgcf", "cae", acc)
    report("abcabdebac", "cda", acc)
    report("bba", "ab", acc)
    report("aaaaaaaaaab", "b", acc)
    report("ADOBECODEBANC", "ABCC", acc)
    print("sums: " + " ".join(acc))


if __name__ == "__main__":
    main()
