# Python mirror of hills.kara (LeetCode #2210, the ★ arm): one pass
# keeping the last number that differs from the current one; a number is
# skipped while the next is equal, so a run counts once, at its end,
# against the last different number before it and the next after.


def count_hill_valley(nums):
    count = 0
    left = nums[0]
    for i in range(1, len(nums) - 1):
        if nums[i] == nums[i + 1]:
            continue
        right = nums[i + 1]
        if (nums[i] > left and nums[i] > right) or (nums[i] < left and nums[i] < right):
            count += 1
        if nums[i] != left:
            left = nums[i]
    return count


# ---- test harness ---------------------------------------------------------

seed = 2210


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(nums):
    print(f"[{', '.join(map(str, nums))}] -> {count_hill_valley(nums)}")


def main():
    # LeetCode's two examples, then four more: three numbers alike, a
    # plateau as a hill, a valley at either end that does not count, and
    # a zigzag
    show([2, 4, 1, 1, 6, 5])
    show([6, 6, 5, 5, 4, 1])
    show([7, 7, 7])
    show([1, 3, 3, 3, 2])
    show([1, 5, 5, 1, 1, 5, 5])
    show([1, 2, 1, 2, 1, 2, 1])
    # 3000 random arrays of 3 to 30 numbers up to 3, 10 and 100 in turn
    most = 0
    check = 0
    for c in range(3000):
        n = next_random() % 28 + 3
        top = [3, 10, 100][c % 3]
        nums = [next_random() % top + 1 for _ in range(n)]
        found = count_hill_valley(nums)
        most = max(most, found)
        check = (check * 31 + found) % 1000000007
    print(f"3000 arrays: most {most}, checksum {check}")
    # the constraints' longest: 100 numbers, a zigzag of 1 and 100, every
    # number in pairs, and 100 alike
    zigzag = [1 if i % 2 == 0 else 100 for i in range(100)]
    pairs = [1 if i // 2 % 2 == 0 else 100 for i in range(100)]
    flat = [100] * 100
    print(f"zigzag {count_hill_valley(zigzag)}, pairs {count_hill_valley(pairs)}, flat {count_hill_valley(flat)}")


main()
