# LeetCode #862: Shortest Subarray with Sum at Least K -- Python mirror of
# the ★ arm (prefix sums and a deque of candidate starts).
from collections import deque


def shortest_subarray(nums, k):
    n = len(nums)
    p = [0]
    for x in nums:
        p.append(p[-1] + x)
    best = n + 1
    starts = deque()
    for j in range(n + 1):
        while starts and p[j] - p[starts[0]] >= k:
            best = min(best, j - starts[0])
            starts.popleft()
        while starts and p[starts[-1]] >= p[j]:
            starts.pop()
        starts.append(j)
    return best if best <= n else -1


def show(nums, k):
    print(f"{nums}, k = {k} -> {shortest_subarray(nums, k)}")


seed = 862


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    for nums, k in [([1], 1), ([1, 2], 4), ([2, -1, 2], 3), ([5], 5), ([-5], 1), ([1, 1, 1, 1], 4),
                    ([1, -1, 1, -1, 5], 5), ([10, -20, 10, 10], 20), ([84, -37, 32, 40, 95], 167),
                    ([-28, 81, -20, 28, -29], 89), ([17, 85, 93, -45, -21], 150),
                    ([2, -1, 2, -1, 2, -1, 2], 4), ([3, -2, 5, -9, 4, 4], 8),
                    ([1, 2, 3, -100, 1, 2, 3, 4], 10)]:
        show(nums, k)
    queries = 0
    none = 0
    total = 0
    count = 5
    for n in range(1, 6):
        for code in range(count):
            nums = []
            c = code
            for _ in range(n):
                nums.append(c % 5 - 2)
                c //= 5
            for k in range(1, 5):
                got = shortest_subarray(nums, k)
                queries += 1
                if got < 0:
                    none += 1
                else:
                    total += got
        count *= 5
    print(f"all {queries} small queries: {none} without a subarray, the rest sum to {total}")
    found = 0
    check = 0
    for _ in range(500):
        n = 1 + next_random() % 100
        nums = [next_random() % 201 - 100 for _ in range(n)]
        k = 1 + next_random() % 1000
        got = shortest_subarray(nums, k)
        if got > 0:
            found += 1
        check = (check * 31 + got + 2) % 1000000007
    print(f"500 random arrays: {found} with a subarray, checksum {check}")


main()
