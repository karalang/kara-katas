# LeetCode #2401: Longest Nice Subarray -- the bench, the ★ arm in Python:
# a sliding window keeping the OR of its values, values leaving from the
# left by XOR until the new one fits.

seed = 2401


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def longest_nice_subarray(nums):
    used = 0
    left = 0
    best = 0
    for right in range(len(nums)):
        while used & nums[right] != 0:
            used ^= nums[left]
            left += 1
        used |= nums[right]
        if right - left + 1 > best:
            best = right - left + 1
    return best


def main():
    arrays = []
    for _ in range(20):
        nums = []
        for _ in range(100000):
            x = 1 << (next_random() % 30)
            if next_random() % 2 == 0:
                x |= 1 << (next_random() % 30)
            nums.append(x)
        arrays.append(nums)
    check = 0
    for p in range(20):
        for nums in arrays:
            check = (check * 31 + longest_nice_subarray(nums) + p) % 1000000007
    print(f"20 passes over 20 arrays of 10^5 values: checksum {check}")


main()
