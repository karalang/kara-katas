# LeetCode #2223: Sum of Scores of Built Strings -- bench mirror of
# scores.kara: the Z-function by the Z-algorithm, z[0] = n, summed.


def sum_scores(s):
    n = len(s)
    z = [0] * n
    z[0] = n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l = i
            r = i + z[i]
    return sum(z)


seed = 2223


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letter():
    return 'b' if next_random() % 2 == 1 else 'a'


def main():
    # 10^5 letters, each 'a' or 'b'
    words = [[letter() for _ in range(100000)] for _ in range(20)]
    check = 0
    for word in words:
        for r in range(5):
            # punch: one letter is drawn again before each answer
            word[r * 19999] = letter()
            s = "".join(word)
            check = (check * 31 + sum_scores(s)) % 1000000007
    print(f"20 strings of 10^5, 5 punches: checksum {check}")


main()
