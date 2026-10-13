# Benchmark for #519: Python mirror of the ★ arm (a shuffle kept in a
# dict); see random_flip_matrix.kara.


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


seed = 519


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 10,000 grids of up to 10,000 by 10,000, 1,000 calls on each: a
    # reset one time in a hundred and whenever the grid is full, else a
    # flip.
    checksum = 0
    grids = 10000
    for g in range(grids):
        high = next_random()
        m = 1 + (high * 32768 + next_random()) % 10000
        high = next_random()
        n = 1 + (high * 32768 + next_random()) % 10000
        solution = Solution(m, n, g)
        free = m * n
        for _ in range(1000):
            if free == 0 or next_random() % 100 == 0:
                solution.reset()
                free = m * n
            else:
                p = solution.flip()
                free -= 1
                checksum = (checksum * 31 + p[0] * 10000 + p[1]) % 1000000007
    print(f"{grids} grids, 1000 calls each: checksum {checksum}")


main()
