# Benchmark for #376 -- mirror of wiggle.kara.


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


def main():
    seed = 376
    checksum = 0
    nums = [0] * 1000
    for case in range(20000):
        top = 6 if case % 3 == 0 else 1001
        for i in range(1000):
            seed = (seed * 1103515245 + 12345) % 2147483648
            nums[i] = (seed // 65536) % top
        checksum = (checksum * 1009 + wiggle_max_length(nums)) % 1000000007
    print(f"checksum {checksum}")


main()
