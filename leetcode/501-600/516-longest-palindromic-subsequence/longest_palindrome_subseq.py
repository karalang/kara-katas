# LeetCode #516: Longest Palindromic Subsequence -- a table over
# substrings. Mirrors longest_palindrome_subseq.kara (the star arm) and
# its harness.


def longest_palindrome_subseq(s):
    b = s.encode()
    n = len(b)
    best = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        best[i][i] = 1
        for j in range(i + 1, n):
            if b[i] == b[j]:
                best[i][j] = best[i + 1][j - 1] + 2
            else:
                best[i][j] = max(best[i + 1][j], best[i][j - 1])
    return best[0][n - 1]


# ---- test harness ---------------------------------------------------------

seed = 516


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(s):
    print(f'"{s}": {longest_palindrome_subseq(s)}')


def main():
    show("bbbab")
    show("cbbd")
    show("a")
    show("abcde")
    show("racecar")
    show("character")
    show("abacabadabacabaeabacabadabacaba")
    count = 300
    total = 0
    checksum = 0
    for t in range(count):
        letters = 2 if t % 3 == 0 else 5 if t % 3 == 1 else 26
        n = 1 + next_random() % 80
        s = "".join(chr(97 + next_random() % letters) for _ in range(n))
        v = longest_palindrome_subseq(s)
        total += v
        checksum = (checksum * 31 + v) % 1000000007
    print(f"{count} random strings: {total} in all, checksum {checksum}")


main()
