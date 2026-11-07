# LeetCode #2002: Maximum Product of the Length of Two Palindromic
# Subsequences -- the benchmark, the same algorithm as palindromes.kara.


def longest_palindrome(chars):
    n = len(chars)
    if n == 0:
        return 0
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            if chars[i] == chars[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1]


def max_product(s):
    b = s.encode()
    n = len(b)
    best = 0
    for mask in range(1, 1 << n):
        picked = []
        rest = []
        for i in range(n):
            if mask >> i & 1:
                picked.append(b[i])
            else:
                rest.append(b[i])
        if picked == picked[::-1]:
            best = max(best, len(picked) * longest_palindrome(rest))
    return best


seed = 2002


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    strings = []
    for a in range(3000):
        strings.append("".join(chr(97 + next_random() % (2 + a % 4)) for _ in range(12)))
    total = check = 0
    for s in strings:
        answer = max_product(s)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"{len(strings)} strings: sum {total}, checksum {check}")


main()
