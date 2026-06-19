"""LeetCode #44: Wildcard Matching — known-correct reference oracle.

Match the ENTIRE string `s` against pattern `p`, where `?` matches any single character and
`*` matches any sequence of characters (including the empty one). Unlike #10, `.` is a literal
character here and `*` is a free-standing wildcard (not a quantifier bound to the previous
char).

Three styles, all returning the IDENTICAL answer for every case (cross-checked below), each
mirroring one Kāra pedagogical file:

  - Style 1 (greedy two pointers with star backtracking, O(1) space, ★) — wildcard_matching.kara
  - Style 2 (bottom-up 2D DP table, O(m·n) space)                       — wildcard_matching_dp2d.kara
  - Style 3 (rolling 1D DP, O(n) space)                                 — wildcard_matching_dp1d.kara

Output is the bare boolean per case, printed lowercase (`true`/`false`) so it is line-for-line
diffable against each Kāra mirror's stdout under both `karac run` and `karac build`.
"""

from __future__ import annotations


# --- Style 1: greedy two pointers with star backtracking (mirrors wildcard_matching.kara, ★) -
#
# Walk one pointer in each string; remember the last '*' and the s-position it was aligned to,
# so a dead end rewinds to "let that '*' eat one more char" instead of re-searching. O(1) space.

def is_match_greedy(s: str, p: str) -> bool:
    n, m = len(s), len(p)
    i = j = 0
    star = -1
    matched = 0
    while i < n:
        if j < m and (p[j] == "?" or p[j] == s[i]):
            i += 1
            j += 1
        elif j < m and p[j] == "*":
            star = j
            matched = i
            j += 1
        elif star != -1:
            matched += 1
            i = matched
            j = star + 1
        else:
            return False
    while j < m and p[j] == "*":
        j += 1
    return j == m


# --- Style 2: bottom-up 2D DP table (mirrors wildcard_matching_dp2d.kara) ------------------
#
# dp[i][j] = does s[:i] match p[:j]. '*' carries left (match empty) or up (absorb one char);
# '?'/literal carries the diagonal. O(m·n) time and space.

def is_match_dp2d(s: str, p: str) -> bool:
    n, m = len(s), len(p)
    dp = [[False] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = True
    for j in range(1, m + 1):
        if p[j - 1] == "*":
            dp[0][j] = dp[0][j - 1]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if p[j - 1] == "*":
                dp[i][j] = dp[i - 1][j] or dp[i][j - 1]
            elif p[j - 1] == "?" or p[j - 1] == s[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]
    return dp[n][m]


# --- Style 3: rolling 1D DP (mirrors wildcard_matching_dp1d.kara) --------------------------
#
# Two rows of the 2D table: prev (row i-1) and curr (row i), rolled after each s char. O(n)
# space.

def is_match_dp1d(s: str, p: str) -> bool:
    n, m = len(s), len(p)
    prev = [False] * (m + 1)
    curr = [False] * (m + 1)
    prev[0] = True
    for j in range(1, m + 1):
        if p[j - 1] == "*":
            prev[j] = prev[j - 1]
    for i in range(1, n + 1):
        curr[0] = False
        for c in range(1, m + 1):
            if p[c - 1] == "*":
                curr[c] = prev[c] or curr[c - 1]
            elif p[c - 1] == "?" or p[c - 1] == s[i - 1]:
                curr[c] = prev[c - 1]
            else:
                curr[c] = False
        prev = curr[:]
    return prev[m]


def report(s: str, p: str) -> None:
    a = is_match_greedy(s, p)
    b = is_match_dp2d(s, p)
    c = is_match_dp1d(s, p)
    assert a == b == c, (s, p, a, b, c)
    print("true" if a else "false")


def main() -> None:
    report("aa", "a")
    report("aa", "*")
    report("cb", "?a")
    report("adceb", "*a*b")
    report("acdcb", "a*c?b")

    report("", "")
    report("", "*")
    report("", "?")
    report("", "***")

    report("abc", "???")
    report("abc", "??")
    report("abc", "*c")
    report("abc", "a*")

    report("aaaa", "***a")
    report("abcabczzzde", "*abc???de*")
    report("mississippi", "m*si?p*.")


if __name__ == "__main__":
    main()
