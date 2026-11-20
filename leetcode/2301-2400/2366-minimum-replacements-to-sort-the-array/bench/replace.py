# LeetCode #2366: Minimum Replacements to Sort the Array -- the bench, the
# ★ arm in Python: greedy from the right, a value over the bound split
# into the fewest pieces that fit, the bound becoming the smallest piece
# of the most even split.


def minimum_replacement(nums):
    n = len(nums)
    bound = nums[n - 1]
    ops = 0
    for i in range(n - 2, -1, -1):
        v = nums[i]
        if v <= bound:
            bound = v
        else:
            k = (v + bound - 1) // bound
            ops += k - 1
            bound = v // k
    return ops


SEED = [2366]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    # array a: 10^5 values from 1 to 10^(a - 1) when a > 0, and a falling
    # run from 10^9 when a is 0
    arrays = []
    top = 1
    for a in range(10):
        if a == 0:
            nums = [1000000000 - i * 9999 for i in range(100000)]
        else:
            nums = []
            for _ in range(100000):
                hi = next_random()
                nums.append(1 + (hi * 32768 + next_random()) % top)
        arrays.append(nums)
        if a > 0:
            top *= 10
    check = 0
    for p in range(100):
        for nums in arrays:
            check = (check * 31 + minimum_replacement(nums) % 1000000007 + p) % 1000000007
    print(f"100 passes over 10 arrays of 10^5 values: checksum {check}")


main()
