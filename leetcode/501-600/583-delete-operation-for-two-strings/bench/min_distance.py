# Benchmark for #583: Python mirror of the ★ arm (the longest common
# subsequence); see min_distance.kara. Each word is made a list of
# characters and the table a list of lists, as in the Kāra arm.


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


# ---- benchmark --------------------------------------------------------------

seed = 583


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def word(length, letters):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    s = ""
    for _ in range(length):
        k = next_random() % letters
        s += alphabet[k:k + 1]
    return s


def main():
    count = 40
    rounds = 30
    firsts = []
    seconds = []
    for _ in range(count):
        letters = 2 + next_random() % 25
        firsts.append(word(500, letters))
        seconds.append(word(500, letters))
    total = 0
    checksum = 0
    for rnd in range(rounds):
        for g in range(count):
            p = (rnd * 7 + g) % count
            got = min_distance(firsts[p], seconds[p])
            total += got
            checksum = (checksum * 31 + got) % 1000000007
    print(f"{count} pairs of 500 letters, {rounds} rounds: {total} deletions, checksum {checksum}")


main()
