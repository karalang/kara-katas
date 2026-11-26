# LeetCode #1771: Maximize Palindrome Length From Subsequences -- the bench
# in Python, mirroring longest_palindrome.kara: the longest palindromic
# subsequence of every stretch of the two words joined.


def longest_palindrome(word1, word2):
    s = (word1 + word2).encode()
    n = len(s)
    split = len(word1)
    dp = [[0] * n for _ in range(n)]
    best = 0
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
                if i < split and j >= split:
                    best = max(best, dp[i][j])
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return best


seed = 1771


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    words = []
    for _ in range(100):
        letters = 2 + next_random() % 25
        words.append("".join(chr(97 + next_random() % letters) for _ in range(1000)))
    check = 0
    for call in range(40):
        a = (check + call * 7919) % 100
        b = (check // 100 + call * 31 + 1) % 100
        check = (check * 31 + longest_palindrome(words[a], words[b])) % 1000000007
    print(f"40 calls over 100 words: checksum {check}")


main()
