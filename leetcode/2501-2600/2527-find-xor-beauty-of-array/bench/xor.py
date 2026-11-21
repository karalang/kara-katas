# LeetCode #2527: Find Xor-Beauty of Array -- benchmark mirror of the ★
# arm (xor.kara): 1000 lists of 100 numbers built once, then the passes,
# each asking every list from an offset the checksum picks.


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
    lists = []
    for _ in range(1000):
        lists.append([wide_random() % 1000000000 + 1 for _ in range(100)])
    passes = 3000
    check = 0
    for p in range(passes):
        start = check % 1000
        for i in range(1000):
            check = (check * 31 + xor_beauty(lists[(start + i) % 1000]) + p) % 1000000007
    print(f"{passes} passes over 1000 lists of 100 numbers: checksum {check}")


main()
