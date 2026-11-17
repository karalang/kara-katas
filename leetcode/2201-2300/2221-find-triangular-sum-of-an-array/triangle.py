# LeetCode #2221: Find Triangular Sum of an Array -- mirror of
# triangle.kara: the rounds done in place, each writing
# (nums[i] + nums[i + 1]) % 10 over nums[i]. O(n^2).


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


def show(nums):
    print(f"{nums} -> {triangular_sum(nums)}")


def main():
    # LeetCode's two examples, then four more: two nines, all zeros, a
    # lone 1 at the start of eight, and 1 to 9
    show([1, 2, 3, 4, 5])
    show([5])
    show([9, 9])
    show([0, 0, 0, 0])
    show([1, 0, 0, 0, 0, 0, 0, 0])
    show([1, 2, 3, 4, 5, 6, 7, 8, 9])
    # 3000 random arrays of 1 to 40 digits
    check = 0
    for _ in range(3000):
        n = next_random() % 40 + 1
        nums = [next_random() % 10 for _ in range(n)]
        check = (check * 31 + triangular_sum(nums)) % 1000000007
    print(f"3000 arrays: checksum {check}")
    # the constraints' largest: 1000 random digits, and 1000 nines
    wide = [next_random() % 10 for _ in range(1000)]
    nines = [9] * 1000
    print(f"1000 random digits: {triangular_sum(wide)}; 1000 nines: {triangular_sum(nines)}")


main()
