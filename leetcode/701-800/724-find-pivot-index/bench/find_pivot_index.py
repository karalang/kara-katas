# LeetCode #724: Find Pivot Index -- the total, then one running sum.
# Benchmark mirror of the Kara star arm: the total once, then a walk
# from the left keeping the sum of the numbers passed, stopping at the
# first index whose left sum equals what is left on the right.


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def pivot_index(nums):
    total = 0
    for x in nums:
        total += x
    left = 0
    for i in range(len(nums)):
        if left == total - left - nums[i]:
            return i
        left += nums[i]
    return -1


def main():
    seed = [724]
    arrays = []
    for _ in range(50):
        nums = []
        for _ in range(4999):
            nums.append(next_random(seed) % 2001 - 1000)
        nums.append(next_random(seed) % 2001 - 1000)
        for j in range(4999):
            nums.append(nums[4998 - j])
        arrays.append(nums)
    total = 0
    for rnd in range(1000):
        for k in range(50):
            p = (rnd * 7919 + k * 31) % 9999
            arrays[k][p] = -arrays[k][p]
            total += pivot_index(arrays[k])
    print(f"1000 rounds of 50 arrays of 9999 numbers: sum {total}")


main()
