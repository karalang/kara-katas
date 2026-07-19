"""LeetCode #132: Palindrome Partitioning II — minimum cuts, O(n^2) DP.

pal[i][j] = s[i..=j] is a palindrome (expand DP). cut[i] = min cuts for the
prefix s[0..=i]: 0 if s[0..=i] itself is a palindrome, else min over j of
cut[j-1]+1 where s[j..=i] is a palindrome. Answer cut[n-1]. Deterministic
scalar output.
"""


def min_cut(s):
    n = len(s)
    if n <= 1:
        return 0
    pal = [[False] * n for _ in range(n)]
    for i in range(n):
        pal[i][i] = True
    for length in range(2, n + 1):
        for i in range(0, n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and (length == 2 or pal[i + 1][j - 1]):
                pal[i][j] = True
    cut = [0] * n
    for i in range(n):
        if pal[0][i]:
            cut[i] = 0
        else:
            best = i  # at most i cuts
            for j in range(1, i + 1):
                if pal[j][i] and cut[j - 1] + 1 < best:
                    best = cut[j - 1] + 1
            cut[i] = best
    return cut[n - 1]


def lcg_str(seed, n, alpha):
    x = seed
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append(chr(ord('a') + (x % alpha)))
    return "".join(out)


def main():
    MOD = 1000000007
    sink = 0
    cases = ["aab", "a", "ab", "aabaa", "abccba", "racecar", "noonabbad",
             "abcde", "aaaaa", "cabababcbc"]
    for s in cases:
        c = min_cut(s)
        print(f"{s}: {c}")
        sink = (sink * 1000003 + c) % MOD
    for t in range(5):
        s = lcg_str(t + 1, 20 + t * 8, 2 + (t % 3))
        c = min_cut(s)
        print(f"lcg{t}(len={len(s)}): {c}")
        sink = (sink * 1000003 + c) % MOD
    print(f"sink: {sink}")


if __name__ == "__main__":
    main()
