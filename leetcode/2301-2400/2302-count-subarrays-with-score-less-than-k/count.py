# LeetCode #2302: Count Subarrays With Score Less Than K -- mirror of the
# ★ arm (count.kara): a sliding window, narrowed at the left while its
# score is k or more, counting every subarray ending at its right end.


def count_subarrays(nums, k):
    count = 0
    total = 0
    left = 0
    for right in range(len(nums)):
        total += nums[right]
        while total * (right - left + 1) >= k:
            total -= nums[left]
            left += 1
        count += right - left + 1
    return count


# ---- test harness ----------------------------------------------------------

seed = 2302


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = [
        ([2, 1, 4, 3, 5], 10),
        ([1, 1, 1], 5),
        ([3, 1, 2], 1),
        ([3, 1, 2], 100),
        ([7], 8),
        ([100000] * 2000, 1000000000000000),
    ]
    for nums, k in cases:
        print(f"n = {len(nums)}, k = {k}: {count_subarrays(nums, k)}")
    check = 0
    total = 0
    for _ in range(2000):
        n = next_random() % 60 + 1
        nums = [next_random() % 20 + 1 for _ in range(n)]
        k = next_random() % 3000 + 1
        c = count_subarrays(nums, k)
        check = (check * 31 + c) % 1000000007
        total += c
    print(f"2000 arrays: checksum {check}, {total} subarrays")


main()
