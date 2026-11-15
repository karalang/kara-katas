# LeetCode #2208: Minimum Operations to Halve Array Sum -- Python mirror of
# the ★ arm: greedily halve the largest number, kept in a heap (`heapq`
# of the numbers negated, so the largest pops first), until the halves
# taken add up to half the sum.
import heapq


def halve_array(nums):
    heap = []
    total = 0.0
    for x in nums:
        total += float(x)
        heapq.heappush(heap, -float(x))
    removed = 0.0
    ops = 0
    while removed < total / 2.0:
        top = -heapq.heappop(heap)
        half = top / 2.0
        removed += half
        heapq.heappush(heap, -half)
        ops += 1
    return ops


# ---- test harness ---------------------------------------------------------

seed = 2208


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    return next_random() * 32768 + next_random()


def show(nums):
    print(f"{nums} -> {halve_array(nums)}")


def main():
    show([5, 19, 8, 1])
    show([3, 8, 20])
    show([7])
    show([4, 4])
    show([100, 1, 1, 1])
    show([10000000, 1])
    most = 0
    check = 0
    for c in range(2000):
        n = next_random() % 12 + 1
        top = [10, 1000, 10000000][c % 3]
        nums = [wide_random() % top + 1 for _ in range(n)]
        ops = halve_array(nums)
        most = max(most, ops)
        check = (check * 31 + ops) % 1000000007
    print(f"2000 arrays: most {most}, checksum {check}")
    same = [10000000] * 100000
    print(f"10^5 of 10^7 -> {halve_array(same)}")
    wide = [wide_random() % 10000000 + 1 for _ in range(100000)]
    print(f"10^5 random -> {halve_array(wide)}")
    lone = [1] * 100000
    lone[50000] = 10000000
    print(f"10^7 among 99999 ones -> {halve_array(lone)}")


main()
