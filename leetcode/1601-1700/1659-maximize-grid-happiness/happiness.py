# LeetCode #1659: Maximize Grid Happiness -- the Python mirror of the ★
# arm: a memoised search over the cells in reading order, keeping the last
# n choices as a base-3 number.

import sys

sys.setrecursionlimit(10000)

INTROVERT = 1
EXTROVERT = 2


def pair(a, b):
    if a == 0 or b == 0:
        return 0
    return sum(-30 if p == INTROVERT else 20 for p in (a, b))


def get_max_grid_happiness(m, n, introverts_count, extroverts_count):
    top = 3**n
    memo = {}

    def best(cell, introverts, extroverts, last):
        if cell == m * n or (introverts == 0 and extroverts == 0):
            return 0
        key = (cell, introverts, extroverts, last)
        if key in memo:
            return memo[key]
        up = last // (top // 3)
        left = 0 if cell % n == 0 else last % 3
        shifted = last % (top // 3) * 3
        result = best(cell + 1, introverts, extroverts, shifted)
        if introverts > 0:
            gain = 120 + pair(INTROVERT, up) + pair(INTROVERT, left)
            result = max(result, gain + best(cell + 1, introverts - 1, extroverts, shifted + INTROVERT))
        if extroverts > 0:
            gain = 40 + pair(EXTROVERT, up) + pair(EXTROVERT, left)
            result = max(result, gain + best(cell + 1, introverts, extroverts - 1, shifted + EXTROVERT))
        memo[key] = result
        return result

    return best(0, introverts_count, extroverts_count, 0)


# ---- the harness: the same as every arm's ---------------------------------

seed = 1659


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, most, people):
    check = 0
    total = 0
    for _ in range(count):
        m = next_random() % most + 1
        n = next_random() % most + 1
        introverts = next_random() % (people + 1)
        extroverts = next_random() % (people + 1)
        answer = get_max_grid_happiness(m, n, introverts, extroverts)
        total += answer
        check = (check * 31 + answer + 1) % 1000000007
    print(f"{count} grids up to {most} by {most} with up to {people} of each: happiness sums to {total}, checksum {check}")


print(get_max_grid_happiness(2, 3, 1, 2))
print(get_max_grid_happiness(3, 1, 2, 1))
print(get_max_grid_happiness(2, 2, 4, 0))
print(get_max_grid_happiness(4, 4, 0, 0))
print(get_max_grid_happiness(1, 5, 2, 3))
print(get_max_grid_happiness(5, 5, 6, 6))
batch(300, 3, 3)
batch(200, 5, 6)
