# LeetCode #456: 132 Pattern -- mirror of pattern132.kara (one stack,
# from the right), with the same harness.


def find132pattern(nums):
    stack = []
    third = -(2**63)
    for i in range(len(nums) - 1, -1, -1):
        if nums[i] < third:
            return True
        while stack and stack[-1] < nums[i]:
            third = stack.pop()
        stack.append(nums[i])
    return False


# ---- test harness ---------------------------------------------------------


def listed(nums):
    return ",".join(str(x) for x in nums)


def show(nums):
    print(f"[{listed(nums)}]: {'true' if find132pattern(nums) else 'false'}")


seed = 456


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show([1, 2, 3, 4])
    show([3, 1, 4, 2])
    show([-1, 3, 2, 0])
    show([5])
    show([1, 2])
    show([1, 3, 3])
    show([1, 3, 1])
    show([3, 5, 0, 3, 4])
    show([-1000000000, 1000000000, 999999999])
    show([9, 8, 7, 6])
    # 300 random arrays of 1 to 200 numbers over 2, 5, 50 or every value
    # from -10^9 to 10^9; the first 100 are sorted upward, except for a
    # few numbers moved, so that the pattern is not always present.
    count = 300
    found = 0
    checksum = 0
    for case in range(count):
        n = 1 + next_random() % 200
        spread = [2, 5, 50, 2000000001][next_random() % 4]
        nums = []
        for _ in range(n):
            r = next_random() * 65536
            r += next_random()
            nums.append(r % spread - spread // 2)
        if case < 100:
            nums.sort()
            for _ in range(next_random() % 3):
                at = next_random() % n
                to = next_random() % n
                nums[at], nums[to] = nums[to], nums[at]
        has = find132pattern(nums)
        if has:
            found += 1
        checksum = (checksum * 31 + (case + 1 if has else 0)) % 1000000007
    print(f"{count} random arrays: {found} with the pattern, checksum {checksum}")


main()
