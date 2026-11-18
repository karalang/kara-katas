# LeetCode #1608: Special Array With X Elements Greater Than or Equal X --
# the bench in Python, mirroring special.kara: the numbers sorted largest
# first, `x` special when the `x`th largest is at least `x` and the next
# is below it.


def special_array(nums):
    nums = sorted(nums, reverse=True)
    n = len(nums)
    for x in range(1, n + 1):
        if nums[x - 1] >= x and (x == n or nums[x] < x):
            return x
    return -1


def main():
    seed = 1608

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    problems = []
    for _ in range(1000):
        nums = []
        for _ in range(10000):
            a = next_random()
            nums.append((a * 32768 + next_random()) % 10001)
        problems.append(nums)
    check = special = 0
    for nums in problems:
        x = special_array(nums)
        if x >= 0:
            special += 1
        check = (check * 31 + x + 1) % 1000000007
    print(f"1000 problems of 10000 numbers from 0 to 10000: {special} special, checksum {check}")


main()
