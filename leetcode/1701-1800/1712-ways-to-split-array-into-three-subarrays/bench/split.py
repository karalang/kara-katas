# LeetCode #1712: Ways to Split Array Into Three Subarrays -- the Python
# mirror of the bench (split.kara): prefix sums, and for each end of the
# left part two `bisect` searches, on 20 random arrays of 100000 values,
# each answered 10 times.

from bisect import bisect_left, bisect_right


def ways_to_split(nums):
    n = len(nums)
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] + x)
    total = prefix[n]
    ways = 0
    for i in range(1, n - 1):
        left = prefix[i]
        lo = max(bisect_left(prefix, 2 * left), i + 1)
        hi = min(bisect_right(prefix, (total + left) // 2), n)
        if hi > lo:
            ways += hi - lo
    return ways % 1000000007


def next_random(state):
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def main():
    count = 20
    rounds = 10
    n = 100000
    seed = [1712]
    arrays = [[next_random(seed) % 10001 for _ in range(n)] for _ in range(count)]
    total = 0
    check = 0
    for r in range(rounds):
        for nums in arrays:
            answer = ways_to_split(nums)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} arrays of {n} values, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
