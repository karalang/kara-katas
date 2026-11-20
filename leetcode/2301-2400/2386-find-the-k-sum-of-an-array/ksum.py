# LeetCode #2386: Find the K-Sum of an Array -- the Python mirror of
# ksum.kara.

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


seed = 0


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
    global seed
    print(k_sum([2, 4, -2], 5))
    print(k_sum([1, -2, 3, 4, -10, 12], 16))
    print(f"{k_sum([-7], 1)} {k_sum([-7], 2)} {k_sum([7], 1)} {k_sum([7], 2)}")
    print(f"{k_sum([3, -5], 1)} {k_sum([3, -5], 2)} {k_sum([3, -5], 3)} {k_sum([3, -5], 4)}")
    seed = 2386
    big = [wide() % 2000000001 - 1000000000 for _ in range(100000)]
    zeros = [0] * 100000
    print(f"{k_sum(big, 2000)} {k_sum(zeros, 2000)}")
    check = 0
    total = 0
    for _ in range(3000):
        n = 1 + next_random() % 12
        top = 1 + wide() % [1, 10, 1000, 1000000000][next_random() % 4]
        nums = [wide() % (2 * top + 1) - top for _ in range(n)]
        k = 1 + next_random() % min(1 << n, 2000)
        answer = k_sum(nums, k)
        check = (check * 31 + trunc_mod(answer, 1000000007) + 1000000007) % 1000000007
        total += answer
    print(f"3000 arrays: checksum {check}, answers summing to {total}")


if __name__ == "__main__":
    main()
