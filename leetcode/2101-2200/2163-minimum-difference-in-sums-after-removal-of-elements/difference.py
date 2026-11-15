# LeetCode #2163: Minimum Difference in Sums After Removal of Elements --
# the Python mirror of difference.kara, the ★ arm: the n smallest of each
# prefix in a largest-first heap, the n largest of each suffix in a
# smallest-first one.
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


def show(nums):
    print(f"[{', '.join(map(str, nums))}] -> {minimum_difference(nums)}")


def main():
    show([3, 1, 2])
    show([7, 9, 5, 8, 1, 3])
    show([4, 4, 4])
    show([6, 6, 6, 6, 6, 6])
    show([1, 2, 3, 4, 5, 6, 7, 8, 9])
    show([9, 8, 7, 6, 5, 4, 3, 2, 1])
    total = 0
    check = 0
    for rnd in range(2000):
        n = next_random() % 5 + 1
        most = [10, 100, 100000][rnd % 3]
        nums = [wide_random() % most + 1 for _ in range(3 * n)]
        d = minimum_difference(nums)
        total += d
        check = (check * 31 + d + 1000000000) % 1000000007
    print(f"2000 lists: {total} in all, checksum {check}")
    rand = [wide_random() % 100000 + 1 for _ in range(300000)]
    print(f"300000 at random: {minimum_difference(rand)}")
    print(f"300000 the same: {minimum_difference([100000] * 300000)}")


main()
