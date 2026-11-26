# LeetCode #1771: Maximize Palindrome Length From Subsequences -- a Python
# mirror of the ★ arm: the longest palindromic subsequence of every stretch
# of the two words joined, kept where the two end letters match, one in
# each word.


def longest_palindrome(word1, word2):
    s = (word1 + word2).encode()
    n = len(s)
    split = len(word1)
    dp = [[0] * n for _ in range(n)]
    best = 0
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        row, below = dp[i], dp[i + 1] if i + 1 < n else None
        for j in range(i + 1, n):
            if s[i] == s[j]:
                row[j] = below[j - 1] + 2
                if i < split and j >= split:
                    best = max(best, row[j])
            else:
                row[j] = max(below[j], row[j - 1])
    return best


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# n letters from the first `letters` of the alphabet
def random_word(n, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def main():
    global seed
    # LeetCode's three examples
    print(f"{longest_palindrome('cacb', 'cbba')} {longest_palindrome('ab', 'ab')} {longest_palindrome('aa', 'bb')}")
    # the edges
    print(f"{longest_palindrome('a', 'a')} {longest_palindrome('a', 'b')} {longest_palindrome('abc', 'cba')} {longest_palindrome('aaaa', 'a')} {longest_palindrome('xbcd', 'efgx')}")
    # the constraints' most
    seed = 1771
    all_a = "a" * 1000
    w1 = random_word(1000, 26)
    w2 = random_word(1000, 26)
    print(f"the most: {longest_palindrome(all_a, all_a)} {longest_palindrome(w1, w2)}")
    # 3000 random pairs
    check = 0
    for _ in range(3000):
        n1 = 1 + next_random() % 15
        n2 = 1 + next_random() % 15
        letters = 2 + next_random() % 25
        w1 = random_word(n1, letters)
        w2 = random_word(n2, letters)
        check = (check * 31 + longest_palindrome(w1, w2)) % 1000000007
    print(f"3000 random pairs: checksum {check}")


main()
