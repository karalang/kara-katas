# LeetCode #1682: Longest Palindromic Subsequence II -- the bench's Python
# mirror: the ★ arm on 200 random strings of 250 letters from the first 4
# of the alphabet, all drawn first, each answered 2 times.


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


def main():
    count, n, rounds = 200, 250, 2
    alphabet = "abcd"
    strings = ["".join(alphabet[next_random() % 4] for _ in range(n)) for _ in range(count)]
    total = 0
    check = 0
    for r in range(rounds):
        for s in strings:
            answer = longest_palindrome_subseq(s)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} strings of {n} letters, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
