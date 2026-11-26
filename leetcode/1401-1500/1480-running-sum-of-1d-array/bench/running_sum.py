# LeetCode #1480: Running Sum of 1d Array -- bench, Python mirror of
# running_sum.kara


def running_sum(nums):
    sums = []
    total = 0
    for x in nums:
        total += x
        sums.append(total)
    return sums


seed = 1480


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# the remainder with the sign of the dividend, as Kāra's, Rust's, C's and
# Go's `%` gives it
def rem(a, m):
    r = abs(a) % m
    return -r if a < 0 else r


def main():
    arrays = []
    for _ in range(1000):
        nums = []
        for _ in range(1000):
            hi = next_random()
            nums.append((hi * 32768 + next_random()) % 2000001 - 1000000)
        arrays.append(nums)
    check = 0
    for pss in range(200):
        for p in range(1000):
            arrays[p][check % 1000] = (check // 7) % 2000001 - 1000000
            sums = running_sum(arrays[p])
            s = 0
            for j, x in enumerate(sums):
                s += x * (j + 1)
            check = (check * 31 + rem(s, 1000000007) + 1000000007 + pss) % 1000000007
    print(f"200 passes over 1000 arrays of 1000 values: checksum {check}")


main()
