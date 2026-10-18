# LeetCode #712: Minimum ASCII Delete Sum for Two Strings -- a table
# of prefixes.
# Benchmark mirror of the Kara star arm: cost[i][j] is the least ASCII
# sum deleted to make the first i bytes of s1 equal to the first j of
# s2, in a table of rows allocated per call.


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def minimum_delete_sum(s1, s2):
    a = s1.encode()
    b = s2.encode()
    m, n = len(a), len(b)
    cost = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        cost[i][0] = cost[i - 1][0] + a[i - 1]
    for j in range(1, n + 1):
        cost[0][j] = cost[0][j - 1] + b[j - 1]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                cost[i][j] = cost[i - 1][j - 1]
            else:
                drop_a = cost[i - 1][j] + a[i - 1]
                drop_b = cost[i][j - 1] + b[j - 1]
                cost[i][j] = drop_a if drop_a < drop_b else drop_b
    return cost[m][n]


def main():
    seed = [712]
    words = ["".join(chr(97 + next_random(seed) % 26) for _ in range(1000))
             for _ in range(20)]
    total = 0
    for _ in range(10):
        for p in range(10):
            total += minimum_delete_sum(words[2 * p], words[2 * p + 1])
    print(f"10 rounds of 10 pairs of 1000 letters: sum {total}")


main()
