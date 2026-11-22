# LeetCode #2871: Split Array Into Maximum Number of Subarrays -- the
# Python mirror of the ★ arm (split.kara): a greedy cut each time the
# running AND reaches 0, at least one part.


def max_subarrays(nums):
    parts = 0
    running = -1
    for v in nums:
        running &= v
        if running == 0:
            parts += 1
            running = -1
    return max(parts, 1)


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
    print(f"{max_subarrays([1, 0, 2, 0, 1, 2])} {max_subarrays([5, 7, 1, 3])}")
    n = 100000
    print(f"{max_subarrays([0] * n)} {max_subarrays([1048575] * n)} {max_subarrays([i % 2 + 1 for i in range(n)])}")
    seed = 2871
    total = 0
    check = 0
    for c in range(3030):
        small = c < 3000
        n = next_random() % 8 + 1 if small else wide() % 90001 + 10000
        if small:
            nums = [next_random() % 8 for _ in range(n)]
        elif c % 2 == 0:
            nums = [wide() % 1000001 for _ in range(n)]
        else:
            nums = [(wide() | wide()) % 1000001 for _ in range(n)]
        parts = max_subarrays(nums)
        total += parts
        check = (check * 31 + parts) % 1000000007
        if c == 2999:
            print(f"3000 short arrays: {total} subarrays, checksum {check}")
            total = 0
            check = 0
    print(f"30 long arrays: {total} subarrays, checksum {check}")


main()
