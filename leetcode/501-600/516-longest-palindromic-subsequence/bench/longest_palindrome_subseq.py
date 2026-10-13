# Benchmark for #516: Python mirror of the ★ arm (a table over
# substrings); see longest_palindrome_subseq.kara.


def longest_palindrome_subseq(b):
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


seed = 516


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 120 random strings of 1,000 letters (the problem's most), from the
    # first 4 or all 26 in turn, solved once each.
    strings = 120
    total = 0
    checksum = 0
    for t in range(strings):
        letters = 4 if t % 2 == 0 else 26
        s = bytes(97 + next_random() % letters for _ in range(1000))
        v = longest_palindrome_subseq(s)
        total += v
        checksum = (checksum * 31 + v) % 1000000007
    print(f"{strings} strings of 1000 letters: {total} in all, checksum {checksum}")


main()
