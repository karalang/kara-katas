# LeetCode #1800: Maximum Ascending Subarray Sum -- the ★ arm in Python:
# one pass with the sum of the ascending run that ends here.


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
    print(f"{max_ascending_sum([10, 20, 30, 5, 10, 50])} {max_ascending_sum([10, 20, 30, 40, 50])} {max_ascending_sum([12, 17, 15, 13, 10, 11, 12])}")
    print(" ".join(str(max_ascending_sum(c)) for c in [[7], [5, 5], [9, 7, 5, 3], [3, 2, 1, 2, 3], [1, 2, 3, 3, 4]]))
    flat = [100] * 100
    rising = list(range(1, 101))
    wide = [1 + next_random() % 100 for _ in range(100)]
    print(f"the most: {max_ascending_sum(flat)} {max_ascending_sum(rising)} {max_ascending_sum(wide)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 20
        top = 1 + next_random() % 30
        nums = [1 + next_random() % top for _ in range(n)]
        check = (check * 31 + max_ascending_sum(nums)) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()
