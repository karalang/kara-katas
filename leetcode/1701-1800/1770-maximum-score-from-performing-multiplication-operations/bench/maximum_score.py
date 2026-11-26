# LeetCode #1770: Maximum Score from Performing Multiplication Operations
# -- the bench in Python, mirroring maximum_score.kara: one row of the
# table, filled from the last operation back to the first.


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


seed = 1770


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_numbers(n):
    return [next_random() % 2001 - 1000 for _ in range(n)]


def main():
    numbers = [random_numbers(1000) for _ in range(100)]
    weights = [random_numbers(300) for _ in range(100)]
    check = 0
    for call in range(2000):
        score = maximum_score(numbers[(check + call * 7919) % 100], weights[(check // 100 + call) % 100])
        check = (check * 31 + score % 1000000007 + 1000000007) % 1000000007
    print(f"2000 calls over 100 lists: checksum {check}")


main()
