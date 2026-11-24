# LeetCode #1313 bench, Python: the ★ arm (the list read two numbers at a
# time, each pair's value pushed as many times as its count) on the same
# 100 lists and 2000 passes.


def decompress_rl_elist(nums):
    out = []
    for i in range(0, len(nums), 2):
        for _ in range(nums[i]):
            out.append(nums[i + 1])
    return out


seed = 1313


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    lists = [[1 + next_random() % 100 for _ in range(100)] for _ in range(100)]
    check = 0
    for p in range(2000):
        for nums in lists:
            nums[2 * (check % 50)] = 1 + (check // 7) % 100
            nums[2 * ((check // 11) % 50) + 1] = 1 + (check // 13) % 100
            got = decompress_rl_elist(nums)
            n = len(got)
            check = (check * 31 + n) % 1000000007
            check = (check * 31 + got[check % n]) % 1000000007
            check = (check * 31 + got[(check // 3) % n] + p) % 1000000007
    print(f"2000 passes over 100 lists of 50 pairs: checksum {check}")


main()
