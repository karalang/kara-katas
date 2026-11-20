# LeetCode #1714: Sum Of Special Evenly-Spaced Elements In Array -- the
# Python mirror of the ★ arm (special.kara): the queries taken in order of
# their step; a small step's sums from every start found once, from the
# back, and a large step's walked.

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


def batch(count, most, top, asked, steps, seed):
    total = 0
    check = 0
    for _ in range(count):
        n = next_random(seed) % most + 1
        nums = [wide(seed) % (top + 1) for _ in range(n)]
        q = next_random(seed) % asked + 1
        queries = []
        for _ in range(q):
            x = wide(seed) % n
            queries.append([x, wide(seed) % steps + 1])
        answer = solve(nums, queries)
        for a in answer:
            total += a
            check = (check * 31 + a) % 1000000007
        check = (check * 31 + n + q) % 1000000007
    print(f"{count} problems of up to {most} values and {asked} queries: answers sum to {total}, checksum {check}")


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    # LeetCode's two examples, then one value, a step past the end, and
    # the largest values summed past the modulus
    print(show(solve([0, 1, 2, 3, 4, 5, 6, 7], [[0, 3], [5, 1], [4, 2]])))
    print(show(solve([100, 200, 101, 201, 102, 202, 103, 203], [[0, 7]])))
    print(show(solve([5], [[0, 1], [0, 50000]])))
    print(show(solve([1, 2, 3], [[1, 5], [2, 1]])))
    print(show(solve([1000000000] * 50000, [[0, 1], [1, 2], [49999, 1]])))
    seed = [1714]
    batch(3000, 12, 9, 6, 6, seed)
    batch(300, 1000, 1000000000, 300, 40, seed)
    batch(10, 50000, 1000000000, 1000, 50000, seed)


main()
