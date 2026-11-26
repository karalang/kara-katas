# LeetCode #1770: Maximum Score from Performing Multiplication Operations
# -- a Python mirror of the ★ arm: one row of the table, filled from the
# last operation back to the first.


def maximum_score(nums, multipliers):
    n = len(nums)
    m = len(multipliers)
    best = [0] * (m + 1)
    for i in range(m - 1, -1, -1):
        for left in range(i + 1):
            right = n - 1 - (i - left)
            take_left = multipliers[i] * nums[left] + best[left + 1]
            take_right = multipliers[i] * nums[right] + best[left]
            best[left] = max(take_left, take_right)
    return best[0]


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# n numbers from -bound to bound
def random_numbers(n, bound):
    return [next_random() % (2 * bound + 1) - bound for _ in range(n)]


def main():
    global seed
    # LeetCode's two examples
    print(f"{maximum_score([1, 2, 3], [3, 2, 1])} {maximum_score([-5, -3, -3, -2, 7, 1], [-10, -5, 3, 4, 6])}")
    # the edges
    print(f"{maximum_score([7], [-3])} {maximum_score([1, -2, 3], [-1, -1, -1])} {maximum_score([-4, -1, -9, -2], [-2, -3])} {maximum_score([5, 0, -5], [0, 2])} {maximum_score([1, 1, 1, 100, -100], [1, 10])}")
    # the constraints' most
    seed = 1770
    thousands = [1000] * 100000
    top = [1000] * 300
    nums = random_numbers(100000, 1000)
    multipliers = random_numbers(300, 1000)
    print(f"the most: {maximum_score(thousands, top)} {maximum_score(nums, multipliers)}")
    # 3000 random cases
    check = 0
    for _ in range(3000):
        m = 1 + next_random() % 12
        n = m + next_random() % 11
        bound = 1 + next_random() % 1000
        nums = random_numbers(n, bound)
        multipliers = random_numbers(m, bound)
        check = (check * 31 + maximum_score(nums, multipliers) % 1000000007 + 1000000007) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()
