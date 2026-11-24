# LeetCode #1296: Divide Array in Sets of K Consecutive Numbers -- Python
# mirror of the ★ arm: the counts walked in sorted order, each count left
# starting that many sets.


def is_possible_divide(nums, k):
    if len(nums) % k != 0:
        return False
    count = {}
    for x in nums:
        count[x] = count.get(x, 0) + 1
    for x in sorted(count):
        sets = count[x]
        if sets == 0:
            continue
        for y in range(x, x + k):
            have = count.get(y, 0)
            if have < sets:
                return False
            count[y] = have - sets
    return True


def main():
    seed = 1296

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def problem(groups, k, spread):
        nums = []
        for _ in range(groups):
            a = next_random()
            start = 1 + (a * 32768 + next_random()) % spread
            for d in range(k):
                nums.append(start + d)
        n = len(nums)
        for i in range(n):
            j = i + next_random() % (n - i)
            nums[i], nums[j] = nums[j], nums[i]
        if next_random() % 2 == 0:
            i = next_random() % n
            nums[i] = nums[i] - 1 if nums[i] > 1 and next_random() % 2 == 0 else nums[i] + 1
        return nums

    def b(v):
        return "true" if v else "false"

    print(f"{b(is_possible_divide([1, 2, 3, 3, 4, 4, 5, 6], 4))} {b(is_possible_divide([3, 2, 1, 2, 3, 4, 3, 4, 5, 9, 10, 11], 3))} {b(is_possible_divide([1, 2, 3, 4], 3))} {b(is_possible_divide([5, 5, 7], 1))} {b(is_possible_divide([4, 2, 3, 1], 4))} {b(is_possible_divide([1, 2, 4, 5], 2))} {b(is_possible_divide([1, 2, 2, 3, 3, 4], 3))}")
    yes = 0
    check = 0
    for case in range(3000):
        k = 1 + next_random() % 8
        groups = 1 + next_random() % 40
        spread = [10, 100, 1000000000][case % 3]
        nums = problem(groups, k, spread)
        possible = is_possible_divide(nums, k)
        if possible:
            yes += 1
        check = (check * 131 + (2 if possible else 1)) % 1000000007
    print(f"3000 random arrays: {yes} divide, checksum {check}")


main()
