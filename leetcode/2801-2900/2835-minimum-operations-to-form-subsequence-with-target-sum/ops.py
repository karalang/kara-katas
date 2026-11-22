# LeetCode #2835: Minimum Operations to Form Subsequence With Target Sum
# -- the Python mirror of the ★ arm: counts by bit, low to high, the
# nearest larger power split down when a needed bit has none.


def min_operations(nums, target):
    if sum(nums) < target:
        return -1
    count = [0] * 32
    for x in nums:
        count[(x & -x).bit_length() - 1] += 1
    ops = 0
    for i in range(31):
        if (target >> i) & 1:
            if count[i] > 0:
                count[i] -= 1
            else:
                j = i + 1
                while count[j] == 0:
                    j += 1
                ops += j - i
                count[j] -= 1
                for k in range(i, j):
                    count[k] += 1
        count[i + 1] += count[i] // 2
    return ops


# ---- the harness: the same in every arm --------------------------------

seed = 2835


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    hi = next_random()
    return hi * 32768 + next_random()


def powers(n, top):
    return [1 << (next_random() % (top + 1)) for _ in range(n)]


def main():
    m = min_operations
    print(f"{m([1, 2, 8], 7)} {m([1, 32, 1, 2], 12)} {m([1, 32, 1], 35)}")
    print(f"{m([4, 2, 1], 7)} {m([1073741824], 1)}")
    print(f"{m([1] * 1000, 2147483647)} {m([1073741824] * 1000, 2147483647)}")
    check = 0
    none = 0
    for _ in range(3000):
        n = next_random() % 8 + 1
        nums = powers(n, 5)
        ops = m(nums, next_random() % 64 + 1)
        if ops < 0:
            none += 1
        check = (check * 31 + ops + 1) % 1000000007
    print(f"3000 short arrays: {none} out of reach, checksum {check}")
    check = 0
    none = 0
    for _ in range(300):
        n = next_random() % 1000 + 1
        nums = powers(n, 30)
        ops = m(nums, wide() % 2147483647 + 1)
        if ops < 0:
            none += 1
        check = (check * 31 + ops + 1) % 1000000007
    print(f"300 long arrays: {none} out of reach, checksum {check}")


main()
