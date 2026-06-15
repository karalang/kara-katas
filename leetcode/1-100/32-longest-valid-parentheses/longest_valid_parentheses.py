"""LeetCode #32: Longest Valid Parentheses — known-correct reference oracle.

Algorithmic mirror of longest_valid_parentheses.kara (the index stack). Output
format matches line-for-line so the two can be diffed directly. The two-pass and
dp variants produce identical output; this oracle additionally cross-checks all
three algorithms agree on every case.
"""

from __future__ import annotations


def longest_valid_stack(s: str) -> int:
    stack = [-1]  # base sentinel: the index just before a valid run
    best = 0
    for i, c in enumerate(s):
        if c == "(":
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)  # unmatched ')' — new base
            else:
                best = max(best, i - stack[-1])
    return best


def longest_valid_twopass(s: str) -> int:
    best = 0
    left = right = 0
    for c in s:  # left to right
        if c == "(":
            left += 1
        else:
            right += 1
        if left == right:
            best = max(best, 2 * right)
        elif right > left:
            left = right = 0
    left = right = 0
    for c in reversed(s):  # right to left, mirrored
        if c == "(":
            left += 1
        else:
            right += 1
        if left == right:
            best = max(best, 2 * left)
        elif left > right:
            left = right = 0
    return best


def longest_valid_dp(s: str) -> int:
    n = len(s)
    dp = [0] * n
    best = 0
    for i in range(1, n):
        if s[i] == ")":
            if s[i - 1] == "(":
                dp[i] = (dp[i - 2] if i >= 2 else 0) + 2
            else:
                j = i - dp[i - 1] - 1
                if j >= 0 and s[j] == "(":
                    dp[i] = dp[i - 1] + 2 + (dp[j - 1] if j >= 1 else 0)
            best = max(best, dp[i])
    return best


CASES = [
    "(()", ")()())", "", "(", ")", "(((", ")))", ")(",
    "()", "()()", "(())", "((()))",
    "()(()", "()(())", "(()())", "())(())", ")()())()()(",
    "()(()))(()()", "((((((", "))))))",
]


def main() -> None:
    for s in CASES:
        a = longest_valid_stack(s)
        b = longest_valid_twopass(s)
        c = longest_valid_dp(s)
        assert a == b == c, (s, a, b, c)
        print(f'"{s}" -> {a}')


if __name__ == "__main__":
    main()
