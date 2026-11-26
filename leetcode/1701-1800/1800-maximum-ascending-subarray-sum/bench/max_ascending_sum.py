# LeetCode #1800: Maximum Ascending Subarray Sum -- the bench in Python: the
# ★ arm over 4000 random lists of 100 numbers built once, 400000 calls.


def max_ascending_sum(nums):
    run = nums[0]
    best = run
    for i in range(1, len(nums)):
        if nums[i] > nums[i - 1]:
            run += nums[i]
        else:
            run = nums[i]
        best = max(best, run)
    return best


seed = 1800


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    lists = [[1 + next_random() % 100 for _ in range(100)] for _ in range(4000)]
    check = 0
    for call in range(400000):
        nums = lists[(check + call) % 4000]
        check = (check * 31 + max_ascending_sum(nums)) % 1000000007
    print(f"400000 calls over 4000 lists of 100 numbers: checksum {check}")


main()
