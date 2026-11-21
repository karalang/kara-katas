# LeetCode #2444: Count Subarrays With Fixed Bounds -- the bench, the ★
# arm: one pass keeping the last value outside the bounds, the last min_k
# and the last max_k.


def count_subarrays(nums, min_k, max_k):
    count = 0
    bad = -1
    last_min = -1
    last_max = -1
    for i in range(len(nums)):
        x = nums[i]
        if x < min_k or x > max_k:
            bad = i
        if x == min_k:
            last_min = i
        if x == max_k:
            last_max = i
        count += max(min(last_min, last_max) - bad, 0)
    return count


seed = 2444


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = [[1 + next_random() % 20 for _ in range(100000)] for _ in range(10)]
    check = 0
    for p in range(100):
        for c in range(len(arrays)):
            at = (p * 7919 + c * 104729) % 100000
            arrays[c][at] = 1 + next_random() % 20
            check = (check * 31 + count_subarrays(arrays[c], 3, 17) + p) % 1000000007
    print(f"100 passes over 10 arrays of 10^5 values: checksum {check}")


main()
