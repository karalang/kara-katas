# LeetCode #2527: Find Xor-Beauty of Array -- Python mirror of the ★ arm
# (xor.kara): the xor of every number; the same harness and output.


def xor_beauty(nums):
    beauty = 0
    for x in nums:
        beauty ^= x
    return beauty


seed = 2527


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    return next_random() * 32768 + next_random()


def main():
    fixed = [[1, 4], [15, 45, 20, 2, 34, 35, 5, 44, 32, 30], [1], [1000000000], [7, 7], [1, 2, 3], [1000000000, 999999999, 1], [5, 5, 5]]
    for nums in fixed:
        print(f"[{', '.join(map(str, nums))}] -> {xor_beauty(nums)}")
    for most, top in [(20, 64), (200, 1000000000)]:
        total = 0
        check = 0
        for _ in range(2000):
            n = next_random() % most + 1
            nums = [wide_random() % top + 1 for _ in range(n)]
            a = xor_beauty(nums)
            total += a
            check = (check * 31 + a) % 1000000007
        print(f"2000 random lists of up to {most} numbers to {top}: total {total}, checksum {check}")
    print(f"1 to 10^5: {xor_beauty(list(range(1, 100001)))}")
    random = [wide_random() % 1000000000 + 1 for _ in range(100000)]
    print(f"10^5 random to 10^9: {xor_beauty(random)}")


main()
