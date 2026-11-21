# LeetCode #2461: Maximum Sum of Distinct Subarrays With Length K -- the
# bench, the ★ arm in Python: a sliding window of `k` with a dict
# counting each value in it and the window's sum.


def maximum_subarray_sum(nums, k):
    count = {}
    total = 0
    best = 0
    for i in range(len(nums)):
        count[nums[i]] = count.get(nums[i], 0) + 1
        total += nums[i]
        if i >= k:
            out = nums[i - k]
            count[out] -= 1
            if count[out] == 0:
                del count[out]
            total -= out
        if i + 1 >= k and len(count) == k:
            best = max(best, total)
    return best


seed = 2461


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 10 arrays of 10^5 values from 1 to 2000 built once; then 28
    # passes, each setting one value of every array from the checksum so
    # far, then answering every array with k = 5 + 7 p % 40, folding the
    # answer plus the pass into the checksum
    arrays = [[1 + next_random() % 2000 for _ in range(100000)] for _ in range(10)]
    check = 0
    for p in range(28):
        k = 5 + 7 * p % 40
        for a in range(len(arrays)):
            arrays[a][(check + a) % 100000] = 1 + check % 2000
            check = (check * 31 + maximum_subarray_sum(arrays[a], k) + p) % 1000000007
    print(f"28 passes over 10 arrays of 10^5: checksum {check}")


main()
