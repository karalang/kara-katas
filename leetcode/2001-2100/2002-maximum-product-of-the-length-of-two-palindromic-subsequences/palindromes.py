# LeetCode #2002: Maximum Product of the Length of Two Palindromic
# Subsequences -- the mirror of the ★ arm, palindromes.kara; its output is
# byte-identical.


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
        picked = [b[i] for i in range(n) if mask >> i & 1]
        if picked != picked[::-1]:
            continue
        rest = [b[i] for i in range(n) if not mask >> i & 1]
        best = max(best, len(picked) * longest_palindrome(rest))
    return best


seed = 2002


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_string(n, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def mix(check, answer):
    return (check * 31 + answer) % 1000000007


def main():
    examples = ["leetcodecom", "bb", "accbcaxxcxx", "ab", "aaaaaaaaaaaa",
                "abcdefghijkl", "abacaba", "racecarlevel"]
    for s in examples:
        print(f"{s} -> {max_product(s)}")
    total = check = 0
    for _ in range(1500):
        s = random_string(next_random() % 7 + 2, next_random() % 3 + 1)
        answer = max_product(s)
        total += answer
        check = mix(check, answer)
    print(f"1500 strings of 2 to 8 letters: sum {total}, checksum {check}")
    total = check = 0
    for _ in range(60):
        s = random_string(next_random() % 4 + 9, next_random() % 4 + 2)
        answer = max_product(s)
        total += answer
        check = mix(check, answer)
    print(f"60 strings of 9 to 12 letters: sum {total}, checksum {check}")


main()
