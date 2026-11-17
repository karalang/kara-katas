# LeetCode #2221: Find Triangular Sum of an Array -- bench mirror of
# triangle.kara: the rounds done in place, each writing
# (nums[i] + nums[i + 1]) % 10 over nums[i].


def triangular_sum(nums):
    row = list(nums)
    n = len(row)
    for live in range(n - 1, 0, -1):
        for i in range(live):
            row[i] = (row[i] + row[i + 1]) % 10
    return row[0]


seed = 2221


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 1000 digits, the constraints' largest
    arrays = [[next_random() % 10 for _ in range(1000)] for _ in range(8)]
    check = 0
    for nums in arrays:
        for r in range(8):
            # punch: one digit is drawn again before each answer
            nums[r * 113] = next_random() % 10
            check = (check * 31 + triangular_sum(nums)) % 1000000007
    print(f"8 arrays of 1000 digits, 8 punches: checksum {check}")


main()
