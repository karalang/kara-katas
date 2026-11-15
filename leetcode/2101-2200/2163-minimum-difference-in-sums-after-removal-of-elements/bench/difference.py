# LeetCode #2163: Minimum Difference in Sums After Removal of Elements --
# the benchmark's Python mirror of difference.kara.
import heapq


def minimum_difference(nums):
    n = len(nums) // 3
    kept = []
    s = 0
    left = []
    for i in range(2 * n):
        heapq.heappush(kept, -nums[i])
        s += nums[i]
        if len(kept) > n:
            s += heapq.heappop(kept)
        if i >= n - 1:
            left.append(s)
    kept = []
    s = 0
    best = 2**63 - 1
    for i in range(3 * n - 1, n - 1, -1):
        heapq.heappush(kept, nums[i])
        s += nums[i]
        if len(kept) > n:
            s -= heapq.heappop(kept)
        if i <= 2 * n:
            best = min(best, left[i - n] - s)
    return best


seed = 2163


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    a = next_random()
    return a * 32768 + next_random()


def main():
    lists = [[wide_random() % 100000 + 1 for _ in range(300000)] for _ in range(4)]
    check = 0
    for _ in range(5):
        for k in range(4):
            at = wide_random() % 300000
            lists[k][at] = wide_random() % 100000 + 1
            d = minimum_difference(list(lists[k]))
            check = (check * 31 + d + 1000000000000) % 1000000007
    print(f"20 solves: checksum {check}")


main()
