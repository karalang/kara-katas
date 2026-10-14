# LeetCode #583: Delete Operation for Two Strings -- via the longest
# common subsequence.
#
# Python mirror of min_distance.kara (the starred arm): the fewest
# deletions keep the longest common subsequence, m + n - 2 * lcs.


def min_distance(word1, word2):
    a = list(word1)
    b = list(word2)
    m = len(a)
    n = len(b)
    lcs = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                lcs[i][j] = lcs[i - 1][j - 1] + 1
            else:
                lcs[i][j] = max(lcs[i - 1][j], lcs[i][j - 1])
    return m + n - 2 * lcs[m][n]


# ---- test harness -----------------------------------------------------------

seed = 583


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def word(length, letters):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    return "".join(alphabet[step() % letters] for _ in range(length))


def show(word1, word2):
    print(f"\"{word1}\" and \"{word2}\": {min_distance(word1, word2)}")


def main():
    show("sea", "eat")
    show("leetcode", "etco")
    show("kata", "kata")
    show("abc", "xyz")
    show("a", "a")
    show("a", "b")
    show("subsequence", "sue")
    show("stressed", "desserts")
    show("aaaa", "aa")
    total = 0
    checksum = 0
    for _ in range(300):
        letters = 2 + step() % 3
        m = 1 + step() % 12
        n = 1 + step() % 12
        w1 = word(m, letters)
        w2 = word(n, letters)
        got = min_distance(w1, w2)
        total += got
        checksum = (checksum * 31 + got) % 1000000007
    print(f"300 random pairs: {total} deletions, checksum {checksum}")
    w1 = word(500, 26)
    w2 = word(500, 26)
    print(f"500 and 500, 26 letters: {min_distance(w1, w2)}")
    w3 = word(500, 2)
    w4 = word(500, 2)
    print(f"500 and 500, 2 letters: {min_distance(w3, w4)}")
    print(f"500, the same word: {min_distance(w1, w1)}")
    print(f"500 of a and 500 of b: {min_distance('a' * 500, 'b' * 500)}")


main()
