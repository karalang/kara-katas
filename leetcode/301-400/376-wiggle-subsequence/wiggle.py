# LeetCode #376: Wiggle Subsequence -- mirror of wiggle.kara.


def wiggle_max_length(nums):
    if not nums:
        return 0
    up = down = 1
    for i in range(1, len(nums)):
        if nums[i] > nums[i - 1]:
            up = down + 1
        elif nums[i] < nums[i - 1]:
            down = up + 1
    return max(up, down)


def show(label, nums):
    print(f"{label}: {wiggle_max_length(nums)}")


def main():
    show("example 1", [1, 7, 4, 9, 2, 5])
    show("example 2", [1, 17, 5, 10, 13, 15, 10, 5, 16, 8])
    show("example 3", [1, 2, 3, 4, 5, 6, 7, 8, 9])
    show("one element", [42])
    show("two equal", [3, 3])
    show("two different", [3, 8])
    show("all equal", [5, 5, 5, 5, 5])
    show("plateaus between turns", [1, 4, 4, 4, 2, 2, 7, 7, 3])
    show("strictly falling", [9, 7, 5, 3, 1])
    show("bounds", [0, 1000, 0, 1000, 0])
    seed = 376
    checksum = 0
    for case in range(300):
        seed = (seed * 1103515245 + 12345) % 2147483648
        n = 1 + (seed // 65536) % 1000
        top = 6 if case % 3 == 0 else 1001
        nums = []
        for _ in range(n):
            seed = (seed * 1103515245 + 12345) % 2147483648
            nums.append((seed // 65536) % top)
        checksum = (checksum * 1009 + wiggle_max_length(nums)) % 1000000007
    print(f"300 random arrays: checksum {checksum}")


main()
