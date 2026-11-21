# LeetCode #2455: Average Value of Even Numbers That Are Divisible by
# Three -- bench, Python mirror of average.kara: one pass sums and counts
# the values divisible by 6.


def average_value(nums):
    total = 0
    count = 0
    for x in nums:
        if x % 6 == 0:
            total += x
            count += 1
    return 0 if count == 0 else total // count


seed = 2455


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = [[1 + next_random() % 1000 for _ in range(1000)] for _ in range(1000)]
    check = 0
    for p in range(250):
        for a in range(1000):
            arrays[a][(p * 7919 + a) % 1000] = 1 + check % 1000
            check = (check * 31 + average_value(arrays[a]) + p) % 1000000007
    print(f"250 passes over 1000 arrays of 1000 values: checksum {check}")


main()
