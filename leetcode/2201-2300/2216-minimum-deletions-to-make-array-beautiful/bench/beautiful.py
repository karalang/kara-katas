# LeetCode #2216: Minimum Deletions to Make Array Beautiful -- bench
# mirror of beautiful.kara: a number that would start a pair is deleted
# when the number after it is the same; an odd length left costs one more.


def min_deletion(nums):
    n = len(nums)
    deleted = 0
    for i in range(n - 1):
        if (i - deleted) % 2 == 0 and nums[i] == nums[i + 1]:
            deleted += 1
    if (n - deleted) % 2 == 1:
        deleted += 1
    return deleted


seed = 2216


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# a draw of 30 bits, since one draw stops at 32767
def wide_random():
    return next_random() * 32768 + next_random()


def main():
    arrays = []
    for a in range(60):
        # 10^5 numbers up to 1, 3 and 10^5 in turn
        top = [1, 3, 100000][a % 3]
        arrays.append([wide_random() % (top + 1) for _ in range(100000)])
    check = 0
    for nums in arrays:
        for r in range(20):
            # punch: one number takes its neighbour's value before each answer
            nums[r * 4999 + 1] = nums[r * 4999]
            check = (check * 31 + min_deletion(nums)) % 1000000007
    print(f"60 arrays of 10^5, 20 punches: checksum {check}")


main()
