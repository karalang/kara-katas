# LeetCode #1278 bench, in Python: the ★ arm (the changes for every
# substring, then the fewest for each prefix in each number of pieces) on
# 200 random strings of 100 letters from 2 to 26, each cut into 1 to 100
# pieces, drawn once; 20 rounds, every answer folded into a checksum.


def palindrome_partition(s, k):
    c = list(s)
    n = len(c)
    cost = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            inner = cost[i + 1][j - 1] if length > 2 else 0
            cost[i][j] = inner + (1 if c[i] != c[j] else 0)
    unreachable = n + 1
    best = [[unreachable] * (n + 1) for _ in range(k + 1)]
    best[0][0] = 0
    for p in range(1, k + 1):
        for j in range(p, n + 1):
            for i in range(p - 1, j):
                through = best[p - 1][i] + cost[i][j - 1]
                if through < best[p][j]:
                    best[p][j] = through
    return best[k][n]


seed = 1278


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    cases = []
    for _ in range(200):
        letters = next_random() % 25 + 2
        s = "".join(alphabet[next_random() % letters] for _ in range(100))
        k = next_random() % 100 + 1
        cases.append((s, k))
    check = 0
    for rnd in range(20):
        for s, k in cases:
            check = (check * 131 + palindrome_partition(s, k) + rnd) % 1000000007
    print(f"20 rounds of 200 strings of 100 letters: checksum {check}")


main()
