# LeetCode #1682: Longest Palindromic Subsequence II -- the Python mirror of
# the ★ arm: a table over every stretch of the string and every outer
# letter.


def longest_palindrome_subseq(s):
    letters = [ord(ch) - ord("a") for ch in s]
    n = len(letters)
    best = [[[0] * 26 for _ in range(n)] for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            for c in range(26):
                if letters[i] == c and letters[j] == c:
                    inside = 0
                    if i + 1 < j - 1:
                        for d in range(26):
                            if d != c:
                                inside = max(inside, best[i + 1][j - 1][d])
                    best[i][j][c] = inside + 2
                else:
                    best[i][j][c] = max(best[i + 1][j][c], best[i][j - 1][c])
    if n == 0:
        return 0
    return max(best[0][n - 1])


seed = 1682


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, longest, letters):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    total = 0
    check = 0
    for _ in range(count):
        n = next_random() % longest + 1
        s = "".join(alphabet[next_random() % letters] for _ in range(n))
        answer = longest_palindrome_subseq(s)
        total += answer
        check = (check * 31 + answer + n) % 1000000007
    print(f"{count} strings of up to {longest} letters from {letters}: answers sum to {total}, checksum {check}")


print(longest_palindrome_subseq("bbabab"))
print(longest_palindrome_subseq("dcbccacdb"))
print(longest_palindrome_subseq("a"))
print(longest_palindrome_subseq("aaaa"))
print(longest_palindrome_subseq("abababba"))
batch(3000, 10, 3)
batch(300, 60, 4)
batch(10, 250, 26)
