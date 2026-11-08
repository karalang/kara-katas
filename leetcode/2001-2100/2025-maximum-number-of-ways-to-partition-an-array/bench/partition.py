# LeetCode #2025: Maximum Number of Ways to Partition an Array -- the ★ arm
# in Python, the same algorithm and workload as partition.kara.


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
        best = max(best, right.get(-delta, 0) + seen.get(delta, 0))
    return best


seed = 2025


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = []
    ks = []
    for a in range(20):
        r = [1, 2, 3, 10, 100, 1000, 10000, 100000][a % 8]
        arrays.append([next_random() % (2 * r + 1) - r for _ in range(50000)])
        ks.append(next_random() % (2 * r + 1) - r)
    calls = total = check = 0
    for _ in range(10):
        for a in range(20):
            best = ways_to_partition(arrays[a], ks[a])
            calls += 1
            total += best
            check = (check * 31 + best) % 1000000007
    print(f"{calls} calls: total {total}, checksum {check}")


main()
