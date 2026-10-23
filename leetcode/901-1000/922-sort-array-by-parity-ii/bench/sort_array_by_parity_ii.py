# LeetCode #922: Sort Array By Parity II -- bench: two pointers, in place.
# Mirrors sort_array_by_parity_ii.kara.


def sort_array_by_parity_ii(nums):
    j = 1
    for i in range(0, len(nums), 2):
        if nums[i] % 2 == 1:
            while nums[j] % 2 == 1:
                j += 2
            nums[i], nums[j] = nums[j], nums[i]


seed = 922


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds, n = 3000, 20000
    # n / 2 even and n / 2 odd values up to 1000, shuffled, built once
    original = []
    for k in range(n):
        v = 2 * (next_random() % 500)
        original.append(v if k % 2 == 0 else v + 1)
    i = n - 1
    while i > 0:
        j = next_random() % (i + 1)
        original[i], original[j] = original[j], original[i]
        i -= 1
    check = 0
    for r in range(rounds):
        # a fresh copy each round, rearranged, and one value read back
        nums = list(original)
        sort_array_by_parity_ii(nums)
        check = (check * 1000003 + nums[(r * 7919) % n]) % 1000000007
    print(f"{rounds} rounds over {n} values: checksum {check}")


main()
