# LeetCode #2855: Minimum Right Shifts to Sort the Array -- the Python
# mirror of the ★ arm: at most one drop, and the last value below the
# first, for n - 1 - i shifts.


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


seed = 2855


def nr():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def permutations(n):
    if n == 0:
        return [[]]
    out = []
    for p in permutations(n - 1):
        for at in range(n):
            out.append(p[:at] + [n] + p[at:])
    return out


def main():
    print(minimum_right_shifts([3, 4, 5, 1, 2]), minimum_right_shifts([1, 3, 5]), minimum_right_shifts([2, 1, 4]), minimum_right_shifts([7]))
    s = list(range(1, 101))
    by_one = [100] + list(range(1, 100))
    by_99 = list(range(2, 101)) + [1]
    swapped = s[:]
    swapped[98], swapped[99] = swapped[99], swapped[98]
    print(minimum_right_shifts(s), minimum_right_shifts(by_one), minimum_right_shifts(by_99), minimum_right_shifts(swapped))
    sortable = check = count = 0
    for n in range(1, 8):
        for p in permutations(n):
            shifts = minimum_right_shifts(p)
            count += 1
            sortable += shifts >= 0
            check = (check * 31 + shifts + 1) % 1000000007
    print(f"{count} permutations: {sortable} sortable, checksum {check}")
    sortable = check = 0
    for _ in range(3000):
        n = nr() % 100 + 1
        pool = list(range(1, 101))
        for i in range(100):
            j = i + nr() % (100 - i)
            pool[i], pool[j] = pool[j], pool[i]
        nums = pool[:n]
        if nr() % 3 < 2:
            nums.sort()
            k = nr() % n
            if k:
                nums = nums[-k:] + nums[:-k]
        shifts = minimum_right_shifts(nums)
        sortable += shifts >= 0
        check = (check * 31 + shifts + 1) % 1000000007
    print(f"3000 random arrays: {sortable} sortable, checksum {check}")


main()
