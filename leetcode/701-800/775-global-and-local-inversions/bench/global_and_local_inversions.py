# Benchmark for #775: Global and Local Inversions -- the ★ arm (every
# value at most one place from its index), as the Kāra program does it.


def is_ideal_permutation(nums):
    for i in range(len(nums)):
        if abs(nums[i] - i) > 1:
            return False
    return True


def main():
    count = 64
    n = 100000
    seed = 775

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    perms = []
    for g in range(count):
        nums = list(range(n))
        i = 0
        while i + 1 < n:
            if next_random() % 2 == 0:
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
                i += 2
            else:
                i += 1
        if g % 4 == 1:
            at = n - 4 - next_random() % 1000
            nums[at], nums[at + 3] = nums[at + 3], nums[at]
        elif g % 4 == 2:
            at = next_random() % (n - 3)
            nums[at], nums[at + 3] = nums[at + 3], nums[at]
        perms.append(nums)
    ideals = 0
    checksum = 0
    for rnd in range(12000):
        g = (rnd * 7) % count
        if is_ideal_permutation(perms[g]):
            ideals += 1
            checksum = (checksum * 31 + g + 1) % 1000000007
        else:
            checksum = (checksum * 31 + 7) % 1000000007
    print(f"12000 rounds of {n} values: {ideals} ideal, checksum {checksum}")


main()
