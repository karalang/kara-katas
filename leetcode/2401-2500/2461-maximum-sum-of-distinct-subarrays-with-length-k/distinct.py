# LeetCode #2461: Maximum Sum of Distinct Subarrays With Length K -- the
# Python mirror of distinct.kara: a sliding window of `k` with a dict
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


# ---- test harness ---------------------------------------------------------

seed = 2461


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def show(values):
    return "[" + ", ".join(str(v) for v in values) + "]"


def main():
    cases = [
        ([1, 5, 4, 2, 9, 9, 9], 3),
        ([4, 4, 4], 3),
        ([3, 1, 3], 1),
        ([1, 2, 3, 4], 4),
        ([7, 1, 2, 7], 4),
        ([1, 2, 1, 3, 4, 5], 3),
        ([5, 5, 1, 2, 9, 8], 2),
    ]
    for nums, k in cases:
        print(f"{show(nums)}, k = {k} -> {maximum_subarray_sum(nums, k)}")
    high = [100000 - i for i in range(2000)]
    print(f"2000 distinct from 10^5 down, k = 1000: {maximum_subarray_sum(high, 1000)}")
    print(f"2000 distinct from 10^5 down, k = 2000: {maximum_subarray_sum(high, 2000)}")
    print(f"2000 of 10^5, k = 2: {maximum_subarray_sum([100000] * 2000, 2)}")
    wide = [1 + wide_random() % 100000 for _ in range(100000)]
    for k in (5, 40):
        print(f"10^5 random to 10^5, k = {k}: {maximum_subarray_sum(wide, k)}")
    narrow = [1 + next_random() % 50 for _ in range(100000)]
    print(f"10^5 random to 50, k = 8: {maximum_subarray_sum(narrow, 8)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 12
        nums = [1 + next_random() % 6 for _ in range(n)]
        k = 1 + next_random() % n
        check = (check * 31 + maximum_subarray_sum(nums, k)) % 1000000007
    print(f"3000 random: checksum {check}")


if __name__ == "__main__":
    main()
