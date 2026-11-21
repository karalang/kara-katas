# LeetCode #2419: Longest Subarray With Maximum Bitwise AND -- the bench,
# the ★ arm in Python: one scan keeping the largest value so far and the
# run of it ending here.

seed = 2419


def longest_subarray(nums):
    top = run = best = 0
    for x in nums:
        if x > top:
            top, run, best = x, 0, 0
        if x == top:
            run += 1
            if run > best:
                best = run
        else:
            run = 0
    return best


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = []
    for i in range(10):
        nums = []
        for k in range(100000):
            if k > 0 and next_random() % 2 == 0:
                nums.append(nums[k - 1])
            else:
                nums.append(1 + next_random() % (2 + 100 * i))
        arrays.append(nums)
    check = 0
    for p in range(500):
        for nums in arrays:
            check = (check * 31 + longest_subarray(nums) + p) % 1000000007
    print(f"500 passes over 10 arrays of 10^5 values: checksum {check}")


main()
