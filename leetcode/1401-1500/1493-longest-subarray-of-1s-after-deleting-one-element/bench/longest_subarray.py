# LeetCode #1493: Longest Subarray of 1's After Deleting One Element -- the
# bench in Python, mirroring longest_subarray.kara: a sliding window holding
# at most one 0.


def longest_subarray(nums):
    best = 0
    zeros = 0
    left = 0
    for right in range(len(nums)):
        if nums[right] == 0:
            zeros += 1
        while zeros > 1:
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left)
    return best


def main():
    seed = 1493
    nums = []
    for _ in range(100000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        nums.append(0 if seed // 65536 % 10 == 0 else 1)
    check = 0
    for call in range(1000):
        at = (check + call * 7919) % 100000
        nums[at] = 1 - nums[at]
        check = (check * 31 + longest_subarray(nums) + 1) % 1000000007
    print(f"1000 calls over 100000 digits: checksum {check}")


main()
