# LeetCode #2404: Most Frequent Even Element -- the bench, the ★ arm in
# Python: a dict of counts of the even values, then every entry read for
# the most frequent and the smallest among equal counts.

seed = 2404


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def most_frequent_even(nums):
    count = {}
    for x in nums:
        if x % 2 == 0:
            count[x] = count.get(x, 0) + 1
    best = -1
    most = 0
    for x, c in count.items():
        if c > most or c == most and x < best:
            best = x
            most = c
    return best


def main():
    arrays = [[next_random() % (1 + 50 * i) for _ in range(2000)] for i in range(200)]
    check = 0
    for p in range(100):
        for nums in arrays:
            check = (check * 31 + most_frequent_even(nums) + 1 + p) % 1000000007
    print(f"100 passes over 200 arrays of 2000 values: checksum {check}")


main()
