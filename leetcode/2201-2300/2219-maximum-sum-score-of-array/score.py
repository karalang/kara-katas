# LeetCode #2219: Maximum Sum Score of Array -- mirror of score.kara:
# with the total known, one pass keeps the sum before i, and the sum from
# i on is the total less it. O(n).


def maximum_sum_score(nums):
    total = sum(nums)
    before = 0
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


# n numbers from -top to top
def draw_nums(n, top):
    return [wide_random() % (2 * top + 1) - top for _ in range(n)]


def show(nums):
    print(f"{nums} -> {maximum_sum_score(nums)}")


def main():
    # LeetCode's two examples, then four more: one number, all
    # negative, the best a suffix, and a zero sum
    show([4, 3, -2, 5])
    show([-3, -5])
    show([7])
    show([-4, -1, -9])
    show([-10, 1, 2, 3])
    show([5, -5, 5, -5])
    # 3000 random arrays of 1 to 30 numbers from -3, -100 and -10^5 to
    # 3, 100 and 10^5 in turn
    check = 0
    for c in range(3000):
        n = next_random() % 30 + 1
        nums = draw_nums(n, [3, 100, 100000][c % 3])
        check = (check * 31 + maximum_sum_score(nums) + 3000000) % 1000000007
    print(f"3000 arrays: checksum {check}")
    # the constraints' largest: 10^5 numbers from -10^5 to 10^5, 10^5 of
    # -10^5 and 10^5 of 10^5
    wide = draw_nums(100000, 100000)
    low = [-100000] * 100000
    high = [100000] * 100000
    print(f"10^5 random: {maximum_sum_score(wide)}; 10^5 of -10^5: {maximum_sum_score(low)}; 10^5 of 10^5: {maximum_sum_score(high)}")


main()
