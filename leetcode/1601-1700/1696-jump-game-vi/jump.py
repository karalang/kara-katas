# LeetCode #1696: Jump Game VI -- mirrors jump.kara, the ★ arm: a falling
# deque of the best scores in reach.

from collections import deque


def max_result(nums, k):
    best = [0] * len(nums)
    best[0] = nums[0]
    reach = deque([0])
    for i in range(1, len(nums)):
        if reach[0] < i - k:
            reach.popleft()
        best[i] = nums[i] + best[reach[0]]
        while reach and best[reach[-1]] <= best[i]:
            reach.pop()
        reach.append(i)
    return best[-1]


class Seed:
    def __init__(self, v):
        self.v = v

    def next(self):
        self.v = (self.v * 1103515245 + 12345) % 2147483648
        return self.v // 65536


def batch(count, most, top, reach, seed):
    total = 0
    check = 0
    for _ in range(count):
        n = (seed.next() * 32768 + seed.next()) % most + 1
        nums = [seed.next() % (2 * top + 1) - top for _ in range(n)]
        k = seed.next() % min(n, reach) + 1
        answer = max_result(nums, k)
        total += answer
        # Python's % already lands in [0, 10^9 + 7)
        check = (check * 31 + answer) % 1000000007
    print(f"{count} arrays of up to {most} values within {top}, k up to {reach}: answers sum to {total}, checksum {check}")


def main():
    print(max_result([1, -1, -2, 4, -7, 3], 2))
    print(max_result([10, -5, -2, 4, 0, 3], 3))
    print(max_result([1, -5, -20, 4, -1, 3, -6, -3], 2))
    print(max_result([5], 1))
    print(max_result([1, -1, -1, 1], 1))
    seed = Seed(1696)
    batch(3000, 12, 5, 12, seed)
    batch(300, 1000, 10000, 1000, seed)
    batch(10, 100000, 10000, 100, seed)


main()
