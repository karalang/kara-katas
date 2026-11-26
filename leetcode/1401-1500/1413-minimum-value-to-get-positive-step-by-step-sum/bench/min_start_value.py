def min_start_value(nums, lo, hi):
    total = 0
    lowest = 0
    for i in range(lo, hi):
        total += nums[i]
        lowest = min(lowest, total)
    return 1 - lowest


def main():
    seed = 1413
    pool = []
    for _ in range(100000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        pool.append(seed // 65536 % 201 - 100)
    check = 0
    for _ in range(3000000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        start = seed // 65536 % 99901
        check = (check * 131 + min_start_value(pool, start, start + 100)) % 1000000007
    print(f"3 * 10^6 windows of 100 numbers: checksum {check}")


main()
