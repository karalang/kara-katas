# LeetCode #1659: Maximize Grid Happiness -- the bench's Python mirror:
# the ★ arm on 2000 random problems on grids of 4 to 5 rows by 4 to 5
# columns with up to 6 introverts and 6 extroverts, all drawn first.

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


seed = 1659


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


problems = []
for _ in range(2000):
    m = next_random() % 2 + 4
    n = next_random() % 2 + 4
    introverts = next_random() % 7
    extroverts = next_random() % 7
    problems.append((m, n, introverts, extroverts))
check = 0
total = 0
for m, n, introverts, extroverts in problems:
    answer = get_max_grid_happiness(m, n, introverts, extroverts)
    total += answer
    check = (check * 31 + answer + 1) % 1000000007
print(f"2000 grids of 4 to 5 by 4 to 5: happiness sums to {total}, checksum {check}")
