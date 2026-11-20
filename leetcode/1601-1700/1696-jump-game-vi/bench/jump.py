# LeetCode #1696: Jump Game VI -- the bench's Python mirror: the ★ arm on
# 50 random arrays of 100000 values from -10^4 to 10^4, each with a random
# k up to 100000, all drawn first, each answered 20 times.

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


seed = 1696


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds, n = 50, 20, 100000
    arrays = []
    ks = []
    for _ in range(count):
        arrays.append([next_random() % 20001 - 10000 for _ in range(n)])
        hi = next_random()
        ks.append((hi * 32768 + next_random()) % n + 1)
    total = 0
    check = 0
    for r in range(rounds):
        for c, nums in enumerate(arrays):
            answer = max_result(nums, ks[c])
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} arrays of {n} values, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
