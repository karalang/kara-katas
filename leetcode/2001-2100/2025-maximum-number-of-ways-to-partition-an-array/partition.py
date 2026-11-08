# LeetCode #2025: Maximum Number of Ways to Partition an Array -- a Python
# mirror of the ★ arm (partition.kara): the pivots' differences in two
# dicts, one for each side of the swept index. Same output, byte for byte.


def ways_to_partition(nums, k):
    n = len(nums)
    total = sum(nums)
    d = []
    left = 0
    for p in range(1, n):
        left += nums[p - 1]
        d.append(left - (total - left))
    right = {}
    for x in d:
        right[x] = right.get(x, 0) + 1
    best = right.get(0, 0)
    seen = {}
    for i in range(n):
        if i >= 1:
            x = d[i - 1]
            right[x] = right.get(x, 0) - 1
            seen[x] = seen.get(x, 0) + 1
        delta = k - nums[i]
        ways = right.get(-delta, 0) + seen.get(delta, 0)
        best = max(best, ways)
    return best


seed = 2025


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    examples = [
        ([2, -1, 2], 3),
        ([0, 0, 0], 1),
        ([22, 4, -25, -20, -15, 15, -16, 7, 19, -10, 0, -13, -14], -33),
        ([1, 1], 5),
        ([1, 2], 1),
        ([0, 0, 0, 0, 0], 0),
        ([3, -3, 3, -3], 0),
        ([5, 5, 5, 5], -5),
    ]
    for nums, k in examples:
        print(f"{show(nums)}, {k} -> {ways_to_partition(nums, k)}")
    total = 0
    check = 0
    for _ in range(3000):
        n = next_random() % 19 + 2
        r = next_random() % 5 + 1
        nums = [next_random() % (2 * r + 1) - r for _ in range(n)]
        k = next_random() % (2 * r + 1) - r
        best = ways_to_partition(nums, k)
        total += best
        check = (check * 31 + best) % 1000000007
    print(f"3000 arrays of up to 20 values: total {total}, checksum {check}")
    total = 0
    check = 0
    for a in range(5):
        r = [1, 2, 10, 1000, 100000][a]
        nums = [next_random() % (2 * r + 1) - r for _ in range(1500)]
        k = next_random() % (2 * r + 1) - r
        best = ways_to_partition(nums, k)
        total += best
        check = (check * 31 + best) % 1000000007
    print(f"5 arrays of 1500 values: total {total}, checksum {check}")


main()
