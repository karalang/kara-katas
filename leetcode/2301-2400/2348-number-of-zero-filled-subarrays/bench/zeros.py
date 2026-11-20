# LeetCode #2348: Number of Zero-Filled Subarrays -- the bench, the ★ arm
# in Python: the length of the run of zeros ending at each place, summed.


def zero_filled_subarray(nums):
    run = 0
    total = 0
    for x in nums:
        if x == 0:
            run += 1
        else:
            run = 0
        total += run
    return total


SEED = [2348]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    # array a holds a value that is not zero with a chance of 1 in a + 2
    arrays = []
    for a in range(10):
        nums = []
        for _ in range(100000):
            r = next_random()
            nums.append(r + 1 if r % (a + 2) == 0 else 0)
        arrays.append(nums)
    check = 0
    for p in range(60):
        for nums in arrays:
            check = (check * 31 + zero_filled_subarray(nums) + p) % 1000000007
    print(f"60 passes over 10 arrays of 10^5 values: checksum {check}")


main()
