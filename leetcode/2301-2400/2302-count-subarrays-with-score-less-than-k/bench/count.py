# LeetCode #2302: Count Subarrays With Score Less Than K -- the bench,
# the ★ arm in Python. A sliding window, narrowed at the left while its
# score is k or more, counting every subarray ending at its right end.

seed = 2302


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


def main():
    arrays = []
    for _ in range(20):
        nums = []
        for _ in range(100000):
            hi = next_random()
            nums.append((hi * 32768 + next_random()) % 100000 + 1)
        arrays.append(nums)
    check = 0
    for p in range(30):
        for a in range(20):
            check = (check * 31 + count_subarrays(arrays[a], 1000000000 * (a + 1) + p)) % 1000000007
    print(f"30 passes over 20 arrays of 10^5: checksum {check}")


main()
