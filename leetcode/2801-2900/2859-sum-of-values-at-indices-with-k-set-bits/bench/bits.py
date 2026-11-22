# LeetCode #2859: Sum of Values at Indices With K Set Bits -- the
# bench: the ★ arm over 2000 arrays of 1000 values up to 10^5,
# LeetCode's most, with k up to 10, all drawn first, then each answered
# 100 times.


def sum_indices_with_k_set_bits(nums, k):
    return sum(x for i, x in enumerate(nums) if i.bit_count() == k)


def main():
    count, rounds = 2000, 100
    seed = 2859

    def nr():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def wide():
        a = nr()
        return a * 32768 + nr()

    cases = []
    for _ in range(count):
        k = nr() % 11
        nums = [wide() % 100000 + 1 for _ in range(1000)]
        cases.append((nums, k))
    total = check = 0
    for r in range(rounds):
        for nums, k in cases:
            s = sum_indices_with_k_set_bits(nums, k)
            total += s
            check = (check * 31 + s + r) % 1000000007
    print(f"{count} arrays, {rounds} rounds: sums total {total}, checksum {check}")


main()
