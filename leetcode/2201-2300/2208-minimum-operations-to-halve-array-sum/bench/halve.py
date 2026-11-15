# benchmark's Python mirror of halve.kara (LeetCode #2208, the ★ arm):
# greedily halve the largest number, kept in a heapq of negated floats so
# the largest pops first, until the halves taken add up to half the sum.
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


seed = 2208


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()


def main():
    arrays = []
    for a in range(12):
        top = [10, 1000, 10000000][a % 3]
        arrays.append([wide_random() % top + 1 for _ in range(100000)])
    # each array halved once
    check = 0
    for a in range(12):
        check = (check * 31 + halve_array(arrays[a])) % 1000000007
    print(f"12 arrays of 10^5: checksum {check}")


main()
