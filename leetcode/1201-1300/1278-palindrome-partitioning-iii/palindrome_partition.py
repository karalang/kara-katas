# LeetCode #1278: Palindrome Partitioning III -- Python mirror of the ★
# arm: the changes for every substring, then the fewest for each prefix in
# each number of pieces.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(n, letters):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    return "".join(alphabet[next_random() % letters] for _ in range(n))


def main():
    global seed
    print(f"{palindrome_partition('abc', 2)} {palindrome_partition('aabbc', 3)} {palindrome_partition('leetcode', 8)}")
    seed = 1278
    total = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 30 + 1
        s = random_text(n, next_random() % 3 + 2)
        k = next_random() % n + 1
        got = palindrome_partition(s, k)
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random strings: {total} changes, checksum {check}")
    same = "a" * 100
    alternating = "ab" * 50
    wide = random_text(100, 26)
    print(f"{palindrome_partition(same, 1)} {palindrome_partition(alternating, 1)} {palindrome_partition(alternating, 2)} {palindrome_partition(wide, 1)} {palindrome_partition(wide, 7)} {palindrome_partition(wide, 100)}")


main()
