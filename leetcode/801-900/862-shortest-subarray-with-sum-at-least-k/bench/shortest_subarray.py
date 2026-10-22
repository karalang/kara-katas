# LeetCode #862: Shortest Subarray with Sum at Least K -- Python mirror of
# the bench program (the ★ arm, prefix sums and a deque of candidate
# starts).
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


seed = 862


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_value():
    hi = next_random()
    lo = next_random()
    return (hi * 32768 + lo) % 200001 - 100000


def main():
    n = 100000
    k = 5000000
    rounds = 300
    nums = [random_value() for _ in range(n)]
    total = 0
    check = 0
    for _ in range(rounds):
        hi = next_random()
        lo = next_random()
        i = (hi * 32768 + lo) % n
        old = nums[i]
        nums[i] = random_value()
        got = shortest_subarray(nums, k)
        nums[i] = old
        total += got
        check = (check * 31 + got + 2) % 1000000007
    print(f"{rounds} rounds on {n} values, k = {k}: lengths sum to {total}, checksum {check}")


main()
