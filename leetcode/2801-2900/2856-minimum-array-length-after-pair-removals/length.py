# LeetCode #2856: Minimum Array Length After Pair Removals -- the Python
# mirror of the ★ arm: the longest run m of the sorted array, 2m - n left
# when it is more than half, else n % 2.


def min_length_after_removals(nums):
    n = len(nums)
    most = run = 0
    for i in range(n):
        run = run + 1 if i > 0 and nums[i] == nums[i - 1] else 1
        most = max(most, run)
    return 2 * most - n if 2 * most > n else n % 2


seed = 2856


def nr():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = nr()
    return a * 32768 + nr()


def main():
    print(min_length_after_removals([1, 3, 4, 9]), min_length_after_removals([2, 3, 6, 9]), min_length_after_removals([1, 1, 2]), min_length_after_removals([5]))
    same = [1000000000] * 100000
    most = [1 if i < 50001 else 9 for i in range(100000)]
    print(min_length_after_removals(same), min_length_after_removals(most))
    check = total = 0
    for c in range(3040):
        small = c < 3000
        n = nr() % 8 + 1 if small else wide() % 100000 + 1
        k = 4 if small else nr() % 1000 + 1
        nums = [nr() % k + 1 for _ in range(n)]
        if not small and nr() % 4 == 0:
            run = wide() % (3 * n // 4 + 1)
            v = wide() % 1000000000 + 1
            for i in range(run):
                nums[i] = v
        nums.sort()
        left = min_length_after_removals(nums)
        total += left
        check = (check * 31 + left) % 1000000007
        if c == 2999:
            print(f"3000 short arrays: {total} left, checksum {check}")
            total = check = 0
    print(f"40 long arrays: {total} left, checksum {check}")


main()
