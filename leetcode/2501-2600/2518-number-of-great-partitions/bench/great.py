# LeetCode #2518: Number of Great Partitions -- benchmark mirror of the ★
# arm (great.kara): 20 lists of 1000 numbers built once, then the passes,
# each asking every list with a k the checksum picks.
MOD = 1000000007


def count_partitions(nums, k):
    total = sum(nums)
    if total < 2 * k:
        return 0
    ways = [0] * k
    ways[0] = 1
    all_ = 1
    for x in nums:
        all_ = all_ * 2 % MOD
        if x < k:
            for s in range(k - 1, x - 1, -1):
                ways[s] = (ways[s] + ways[s - x]) % MOD
    short = 0
    for w in ways:
        short = (short + w) % MOD
    return ((all_ - 2 * short) % MOD + MOD) % MOD


seed = 2518


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    lists = [[next_random() % 1000 + 1 for _ in range(1000)] for _ in range(20)]
    passes = 35
    check = 0
    for p in range(passes):
        for nums in lists:
            check = (check * 31 + count_partitions(nums, check % 1000 + 1) + p) % MOD
    print(f"{passes} passes over 20 lists of 1000 numbers: checksum {check}")


main()
