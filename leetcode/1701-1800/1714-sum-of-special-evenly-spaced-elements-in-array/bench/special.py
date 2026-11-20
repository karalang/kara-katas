# LeetCode #1714: Sum Of Special Evenly-Spaced Elements In Array -- the
# Python mirror of the bench (special.kara): the queries taken in order of
# their step, a small step's sums built from the back and a large step's
# walked, on 5 random problems of 50000 values and 150000 queries, each
# answered 4 times.

from math import isqrt

MOD = 1000000007


def solve(nums, queries):
    n = len(nums)
    small = isqrt(n)
    answer = [0] * len(queries)
    order = sorted(range(len(queries)), key=lambda q: queries[q][1])
    sums = [0] * n
    built = 0
    for q in order:
        x, y = queries[q]
        if y <= small:
            if y != built:
                for j in range(n - 1, -1, -1):
                    sums[j] = (nums[j] + (sums[j + y] if j + y < n else 0)) % MOD
                built = y
            answer[q] = sums[x]
        else:
            total = 0
            j = x
            while j < n:
                total += nums[j]
                j += y
            answer[q] = total % MOD
    return answer


def next_random(state):
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def wide(state):
    a = next_random(state)
    return a * 32768 + next_random(state)


def main():
    count = 5
    rounds = 4
    n = 50000
    q = 150000
    seed = [1714]
    problems = []
    for _ in range(count):
        nums = [wide(seed) % 1000000000 for _ in range(n)]
        queries = []
        for _ in range(q):
            x = wide(seed) % n
            if next_random(seed) % 2 == 0:
                y = next_random(seed) % 223 + 1
            else:
                y = wide(seed) % n + 1
            queries.append([x, y])
        problems.append((nums, queries))
    total = 0
    check = 0
    for r in range(rounds):
        for nums, queries in problems:
            for a in solve(nums, queries):
                total += a
                check = (check * 31 + a + r) % 1000000007
    print(f"{count} problems of {n} values and {q} queries, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
