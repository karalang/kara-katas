# LeetCode #2855: Minimum Right Shifts to Sort the Array -- the bench:
# the ★ arm over 10^5 arrays of 100 distinct values up to 100, LeetCode's
# most, two times in three sorted and shifted, else with two values
# swapped after it, all drawn first, then each answered 50 times.


def minimum_right_shifts(nums):
    n = len(nums)
    drop = -1
    for i in range(n - 1):
        if nums[i] > nums[i + 1]:
            if drop >= 0:
                return -1
            drop = i
    if drop < 0:
        return 0
    if nums[n - 1] > nums[0]:
        return -1
    return n - 1 - drop


def main():
    count, rounds = 100000, 50
    seed = 2855

    def nr():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    arrays = []
    for _ in range(count):
        nums = list(range(1, 101))
        k = nr() % 100
        if k:
            nums = nums[-k:] + nums[:-k]
        if nr() % 3 == 2:
            i = nr() % 100
            j = nr() % 100
            nums[i], nums[j] = nums[j], nums[i]
        arrays.append(nums)
    sortable = check = 0
    for r in range(rounds):
        for nums in arrays:
            shifts = minimum_right_shifts(nums)
            if shifts >= 0:
                sortable += 1
            check = (check * 31 + shifts + 1 + r) % 1000000007
    print(f"{count} arrays, {rounds} rounds: {sortable} sortable, checksum {check}")


main()
