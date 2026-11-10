# LeetCode #2090: K Radius Subarray Averages -- Python mirror of the ★ arm
# (averages.kara): one window of 2k + 1 sliding along, its sum over its
# width the average of the place k back. Output is byte-identical.

seed = 2090


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def get_averages(nums, k):
    n = len(nums)
    width = 2 * k + 1
    avgs = [-1] * n
    total = 0
    for i in range(n):
        total += nums[i]
        if i >= width:
            total -= nums[i - width]
        if i + 1 >= width:
            avgs[i - k] = total // width
    return avgs


def show(v):
    return "[" + ",".join(str(x) for x in v) + "]"


def main():
    examples = [
        ([7, 4, 3, 9, 1, 8, 5, 2, 6], 3),
        ([100000], 0),
        ([8], 100000),
        ([1, 2, 3, 4, 5], 1),
        ([5, 5], 1),
        ([0, 0, 0], 0),
        ([1, 2, 3, 4, 5, 6], 2),
    ]
    for nums, k in examples:
        print(f"{show(nums)} {k} -> {show(get_averages(nums, k))}")
    total = check = 0
    for _ in range(2000):
        n = next_random() % 100 + 1
        top = [10, 1000, 100000][next_random() % 3]
        nums = [next_random() % top for _ in range(n)]
        k = next_random() % 60
        for a in get_averages(nums, k):
            total += a
            check = (check * 31 + a + 2) % 1000000007
    print(f"2000 arrays: sum {total}, checksum {check}")
    big = [next_random() % 100001 for _ in range(100000)]
    s = c = 0
    for a in get_averages(big, 10):
        s += a
        c = (c * 31 + a + 2) % 1000000007
    print(f"100000 values, radius 10: sum {s}, checksum {c}")
    one = get_averages(big, 49999)
    missing = sum(1 for a in get_averages(big, 50000) if a == -1)
    print(f"radius 49999: {one[49999]} at 49999, {sum(1 for a in one if a == -1)} missing; radius 50000: {missing} missing")


main()
