# LeetCode #2856: Minimum Array Length After Pair Removals -- the bench:
# the ★ arm over 5000 sorted arrays of 1000 values, each from 1 to k for
# k up to 1000, one time in four with a run of one value making up to
# three quarters, all drawn first, then each answered 50 times.


def min_length_after_removals(nums):
    n = len(nums)
    most = run = 0
    for i in range(n):
        run = run + 1 if i > 0 and nums[i] == nums[i - 1] else 1
        most = max(most, run)
    return 2 * most - n if 2 * most > n else n % 2


def main():
    count, rounds, n = 5000, 50, 1000
    seed = 2856

    def nr():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    arrays = []
    for _ in range(count):
        k = nr() % 1000 + 1
        nums = [nr() % k + 1 for _ in range(n)]
        if nr() % 4 == 0:
            run = nr() % (3 * n // 4 + 1)
            v = nr() % 1000 + 1
            for i in range(run):
                nums[i] = v
        nums.sort()
        arrays.append(nums)
    total = check = 0
    for r in range(rounds):
        for nums in arrays:
            left = min_length_after_removals(nums)
            total += left
            check = (check * 31 + left + r) % 1000000007
    print(f"{count} arrays, {rounds} rounds: {total} left, checksum {check}")


main()
