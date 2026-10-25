# LeetCode #1000: Minimum Cost to Merge Stones -- mirror of the ★ arm
# (merge_stones.kara), an interval table by length.


def merge_stones(stones, k):
    n = len(stones)
    if (n - 1) % (k - 1) != 0:
        return -1
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + stones[i]
    dp = [[0] * n for _ in range(n)]
    for length in range(k, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            best = 1 << 60
            m = i
            while m < j:
                best = min(best, dp[i][m] + dp[m + 1][j])
                m += k - 1
            if (length - 1) % (k - 1) == 0:
                best += prefix[j + 1] - prefix[i]
            dp[i][j] = best
    return dp[0][n - 1]


seed = 1000


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# up to `most` piles of 1 to 100 stones and a k from 2 up: half the time
# a pile count that k can merge down to one pile, half the time any
def random_case(most):
    k = 2 + next_random() % 4
    if next_random() % 2 == 0:
        merges = next_random() % ((most - 1) // (k - 1) + 1)
        n = 1 + merges * (k - 1)
    else:
        n = 1 + next_random() % most
    return [1 + next_random() % 100 for _ in range(n)], k


def main():
    cases = [
        ([3, 2, 4, 1], 2),
        ([3, 2, 4, 1], 3),
        ([3, 5, 1, 2, 6], 3),
        ([7], 2),
        ([7], 5),
        ([4, 6], 2),
        ([4, 6], 3),
        ([1, 2, 3], 3),
        ([6, 4, 4, 6], 2),
        ([1, 100, 1, 100, 1], 3),
    ]
    for stones, k in cases:
        text = ",".join(str(x) for x in stones)
        print(f"stones = [{text}], k = {k} -> {merge_stones(stones, k)}")
    big = [
        ("30 piles of 100, k = 2", [100] * 30, 2),
        ("30 piles of 100, k = 30", [100] * 30, 30),
        ("30 piles of 100, k = 3", [100] * 30, 3),
        ("29 piles of 1 to 29, k = 3", list(range(1, 30)), 3),
        ("29 piles of 1 to 29, k = 15", list(range(1, 30)), 15),
        ("29 piles, 100 and 1 in turn, k = 5", [100 if i % 2 == 0 else 1 for i in range(29)], 5),
    ]
    for name, stones, k in big:
        print(f"{name}: {merge_stones(stones, k)}")
    for count, most in [(300, 6), (3000, 15), (300, 30)]:
        piles = 0
        impossible = 0
        total = 0
        check = 0
        for _ in range(count):
            stones, k = random_case(most)
            got = merge_stones(stones, k)
            piles += len(stones)
            if got < 0:
                impossible += 1
            else:
                total += got
            check = (check * 31 + got + 2) % 1000000007
        print(f"{count} random rows of {piles} piles: {impossible} impossible, cost {total}, checksum {check}")


main()
