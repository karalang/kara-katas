# LeetCode #2386: Find the K-Sum of an Array -- the bench, the ★ arm in
# Python: the largest sum less the (k-1)-th smallest nonempty sum of the
# sorted sizes, walked from the smallest by a heap of (sum, last place).

import heapq


def k_sum(nums, k):
    largest = 0
    sizes = []
    for v in nums:
        if v > 0:
            largest += v
        sizes.append(abs(v))
    sizes.sort()
    heap = [(sizes[0], 0)]
    lost = 0
    for _ in range(1, k):
        total, last = heapq.heappop(heap)
        lost = total
        if last + 1 < len(sizes):
            heapq.heappush(heap, (total + sizes[last + 1], last + 1))
            heapq.heappush(heap, (total - sizes[last] + sizes[last + 1], last + 1))
    return largest - lost


seed = 2386


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    high = next_random()
    return high * 32768 + next_random()


def trunc_mod(a, m):
    # Kara's `%` truncates toward zero, as C's does
    r = abs(a) % m
    return -r if a < 0 else r


def main():
    # 10 arrays of 10^5 values from -10^9 to 10^9; pass p asks array a for
    # k = 2000 - (7 p + a) % 100
    arrays = []
    for _ in range(10):
        arrays.append([wide() % 2000000001 - 1000000000 for _ in range(100000)])
    check = 0
    for p in range(60):
        for a in range(10):
            answer = k_sum(arrays[a], 2000 - (7 * p + a) % 100)
            check = (check * 31 + trunc_mod(answer, 1000000007) + 1000000007 + p) % 1000000007
    print(f"60 passes over 10 arrays of 10^5 values: checksum {check}")


main()
