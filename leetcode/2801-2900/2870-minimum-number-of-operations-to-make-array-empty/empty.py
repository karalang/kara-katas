# LeetCode #2870: Minimum Number of Operations to Make Array Empty --
# the Python mirror of the ★ arm (empty.kara): the sorted array's runs,
# ceil(f / 3) each, -1 on a run of one.


def min_operations(nums):
    s = sorted(nums)
    ops = 0
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        f = j - i
        if f == 1:
            return -1
        ops += (f + 2) // 3
        i = j
    return ops


# ---- the harness: the same in every arm --------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    global seed
    print(f"{min_operations([2, 3, 3, 2, 2, 4, 2, 3, 4])} {min_operations([2, 1, 2, 2, 3, 3])}")
    n = 100000
    print(f"{min_operations([1000000] * n)} {min_operations([i // 2 + 1 for i in range(n)])}")
    seed = 2870
    total = 0
    check = 0
    for c in range(3030):
        small = c < 3000
        if small:
            nums = [next_random() % 4 + 1 for _ in range(next_random() % 9 + 2)]
        else:
            n = wide() % 90001 + 10000
            nums = []
            while len(nums) < n:
                v = wide() % 1000000 + 1
                copies = next_random() % 7 + 2 if c % 2 == 0 else next_random() % 3 + 1
                for _ in range(copies):
                    nums.append(v if c % 2 == 0 else v % (n // 3) + 1)
            for i in range(len(nums) - 1, 0, -1):
                j = wide() % (i + 1)
                nums[i], nums[j] = nums[j], nums[i]
        ops = min_operations(nums)
        total += ops
        check = (check * 31 + ops + 1) % 1000000007
        if c == 2999:
            print(f"3000 short arrays: {total} operations, checksum {check}")
            total = 0
            check = 0
    print(f"30 long arrays: {total} operations, checksum {check}")


main()
