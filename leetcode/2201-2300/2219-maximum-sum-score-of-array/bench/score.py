# LeetCode #2219: Maximum Sum Score of Array -- bench mirror of
# score.kara: with the total known, one pass keeps the sum before i, and
# the sum from i on is the total less it.


def maximum_sum_score(nums):
    total = 0
    for x in nums:
        total += x
    before = 0
    # no score is below the smaller of the first number and the total
    best = min(nums[0], total)
    for x in nums:
        from_here = total - before
        before += x
        best = max(best, before, from_here)
    return best


seed = 2219


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# a draw of 30 bits, since one draw stops at 32767
def wide_random():
    return next_random() * 32768 + next_random()


def main():
    # 10^5 numbers from -10^5 to 10^5
    arrays = [[wide_random() % 200001 - 100000 for _ in range(100000)] for _ in range(30)]
    check = 0
    for nums in arrays:
        for r in range(10):
            # punch: one number is drawn again before each answer
            nums[r * 9999] = wide_random() % 200001 - 100000
            check = (check * 31 + maximum_sum_score(nums) + 10000000000) % 1000000007
    print(f"30 arrays of 10^5, 10 punches: checksum {check}")


main()
