# LeetCode #519: Random Flip Matrix -- mirror of the ★ arm (a shuffle
# kept in a dict); see random_flip_matrix.kara.
import math


class Draw:
    def __init__(self, seed):
        self.seed = seed

    def step(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536

    def below(self, n):
        limit = 1073741824 // n * n
        while True:
            high = self.step()
            low = self.step()
            r = high * 32768 + low
            if r < limit:
                return r % n


class Solution:
    def __init__(self, m, n, seed):
        self.m = m
        self.n = n
        self.free = m * n
        self.moved = {}
        self.draw = Draw(seed)

    def at(self, i):
        return self.moved.get(i, i)

    def flip(self):
        r = self.draw.below(self.free)
        self.free -= 1
        cell = self.at(r)
        last = self.at(self.free)
        self.moved[r] = last
        return [cell // self.n, cell % self.n]

    def reset(self):
        self.moved.clear()
        self.free = self.m * self.n


def fair(counts, weights, total, n):
    for i in range(len(counts)):
        p = weights[i] / total
        sd = math.sqrt(n * p * (1.0 - p))
        if abs(counts[i] - n * p) > 5.0 * sd + 0.000001:
            return False
    return True


def number_of(m, n, p):
    if len(p) != 2 or p[0] < 0 or p[0] >= m or p[1] < 0 or p[1] >= n:
        return -1
    return p[0] * n + p[1]


def b(x):
    return "true" if x else "false"


def permutations(m, n, runs, seed):
    cells = m * n
    solution = Solution(m, n, seed)
    at_turn = [0] * (cells * cells)
    once = True
    for run in range(runs):
        if run > 0:
            solution.reset()
        seen = [False] * cells
        for turn in range(cells):
            k = number_of(m, n, solution.flip())
            if k < 0 or seen[k]:
                once = False
            else:
                seen[k] = True
                at_turn[turn * cells + k] += 1
    even = once
    for turn in range(cells):
        counts = at_turn[turn * cells:(turn + 1) * cells]
        even = even and fair(counts, [1] * cells, cells, runs)
    print(f"{m} by {n}, {runs} times: every cell flipped once {b(once)}, every cell its share at every turn {b(even)}")


_seed = [0]


def next_random():
    _seed[0] = (_seed[0] * 1103515245 + 12345) % 2147483648
    return _seed[0] // 65536


def main():
    solution = Solution(3, 1, 1)
    seen = [False] * 3
    once = True
    for _ in range(3):
        k = number_of(3, 1, solution.flip())
        if k < 0 or seen[k]:
            once = False
        else:
            seen[k] = True
    solution.reset()
    after = number_of(3, 1, solution.flip()) >= 0
    print(f"example: three flips flip every cell {b(once)}, a flip after the reset is a cell {b(after)}")
    solution = Solution(1, 1, 2)
    first = solution.flip()
    solution.reset()
    second = solution.flip()
    print(f"one cell: {first}, then after the reset {second}")
    permutations(1, 7, 2100, 3)
    permutations(3, 1, 900, 4)
    permutations(2, 3, 1800, 5)
    permutations(3, 3, 2700, 6)
    solution = Solution(3, 3, 7)
    first_after = [0] * 9
    distinct = True
    resets = 4500
    for _ in range(resets):
        seen = [False] * 9
        for _ in range(4):
            k = number_of(3, 3, solution.flip())
            if k < 0 or seen[k]:
                distinct = False
            else:
                seen[k] = True
        solution.reset()
        k = number_of(3, 3, solution.flip())
        if k < 0:
            distinct = False
        else:
            first_after[k] += 1
        solution.reset()
    print(f"3 by 3, {resets} resets after 4 flips: the flips different cells {b(distinct)}, the first flip after a reset fair {b(fair(first_after, [1] * 9, 9, resets))}")
    size = 10000
    solution = Solution(size, size, 8)
    seen = set()
    by_row = [0] * 20
    by_column = [0] * 20
    ok = True
    flips = 999
    for _ in range(flips):
        p = solution.flip()
        k = number_of(size, size, p)
        if k < 0 or k in seen:
            ok = False
        else:
            seen.add(k)
            by_row[p[0] // 500] += 1
            by_column[p[1] // 500] += 1
    solution.reset()
    print(f"largest: {flips} flips different cells {b(ok)}, rows even {b(fair(by_row, [1] * 20, 20, flips))}, columns even {b(fair(by_column, [1] * 20, 20, flips))}")
    _seed[0] = 519
    a = Solution(100, 100, 11)
    bb = Solution(100, 100, 11)
    c = Solution(100, 100, 12)
    same = True
    differ = False
    for _ in range(300):
        if next_random() % 50 == 0:
            a.reset()
            bb.reset()
            c.reset()
        pa = a.flip()
        if bb.flip() != pa:
            same = False
        if c.flip() != pa:
            differ = True
    print(f"one seed twice the same {b(same)}, another seed other flips {b(differ)}")


main()
