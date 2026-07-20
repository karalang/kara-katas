"""LeetCode 139 — Word Break (Python mirror / oracle).

DP over prefixes: dp[i] is True when s[:i] segments into dictionary words.
dp[0] is the empty prefix; dp[i] holds if some j < i has dp[j] and s[j:i] is
in the dictionary. Answer is dp[n].
"""


def word_break(s, dict_):
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in dict_:
                dp[i] = True
    return dp[n]


def yes_no(b):
    return "true" if b else "false"


def main():
    print(yes_no(word_break("leetcode", {"leet", "code"})))
    print(yes_no(word_break("applepenapple", {"apple", "pen"})))
    print(yes_no(word_break("catsandog", {"cats", "dog", "sand", "and", "cat"})))
    print(yes_no(word_break("aaaaaaaa", {"a", "aa", "aaa"})))


main()
