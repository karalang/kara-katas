# LeetCode #2518: Number of Great Partitions -- Python mirror of the ★ arm
# (great.kara): 2^n less twice the subsets summing below k, counted by a
# knapsack over the sums below k; and its harness, line for line.
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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def below(top):
    a = next_random()
    b = next_random()
    return (a * 32768 + b) % top


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    global seed
    cases = [([1, 2, 3, 4], 4), ([3, 3, 3], 4), ([6, 6], 2), ([5], 1), ([1, 1], 1), ([1000000000, 1000000000], 1000), ([2, 3, 5, 7, 11], 10), ([1, 2, 3, 4, 5, 6], 11)]
    for nums, k in cases:
        print(f"{show(nums)} k {k} -> {count_partitions(nums, k)}")
    seed = 2518
    for most, top, most_k in [(10, 20, 30), (200, 10, 1000), (200, 1000000000, 1000)]:
        none = 0
        check = 0
        for _ in range(2000):
            n = next_random() % most + 1
            nums = [below(top) + 1 for _ in range(n)]
            k = next_random() % most_k + 1
            a = count_partitions(nums, k)
            if a == 0:
                none += 1
            check = (check * 31 + a) % 1000000007
        print(f"2000 random of up to {most} numbers to {top}: {none} with none, checksum {check}")
    ones = [1] * 1000
    thousands = [1000] * 1000
    run = list(range(1, 1001))
    wide = [below(1000000000) + 1 for _ in range(1000)]
    print(f"1000 ones: {count_partitions(ones, 1000)}")
    print(f"1000 thousands: {count_partitions(thousands, 1000)}")
    print(f"1 to 1000: {count_partitions(run, 1000)}")
    print(f"1000 random to 10^9: {count_partitions(wide, 1000)}")


main()
