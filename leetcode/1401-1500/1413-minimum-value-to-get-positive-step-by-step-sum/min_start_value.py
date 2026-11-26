# LeetCode #1413, Python mirror of min_start_value.kara: the lowest the
# running sum goes, and the start that lifts it to 1.


def min_start_value(nums):
    total = 0
    lowest = 0
    for x in nums:
        total += x
        lowest = min(lowest, total)
    return 1 - lowest


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def drawn(n, top):
    return [next_random() % (2 * top + 1) - top for _ in range(n)]


def main():
    global seed
    firsts = [min_start_value(v) for v in
              [[-3, 2, -3, 4, 2], [1, 2], [1, -2, -3], [0], [-1], [5, -5, 5, -5], [-2, 3, -4, 1]]]
    print(" ".join(str(x) for x in firsts))
    seed = 1413
    low = [-100] * 100
    high = [100] * 100
    print(f"100 numbers: {min_start_value(low)} {min_start_value(high)} {min_start_value(drawn(100, 100))}")
    check = 0
    total = 0
    for _ in range(2000):
        n = 1 + next_random() % 100
        top = 1 + next_random() % 100
        x = min_start_value(drawn(n, top))
        total += x
        check = (check * 131 + x) % 1000000007
    print(f"2000 random arrays: {total} in all, checksum {check}")


main()
