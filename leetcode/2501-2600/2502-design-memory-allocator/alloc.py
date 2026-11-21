# LeetCode #2502: Design Memory Allocator -- mirror of the ★ arm
# (alloc.kara): every unit's owner in a list, 0 for free; allocate scans
# for the first run of `size` free units, free clears every unit of the
# id.


class Allocator:
    def __init__(self, n):
        self.memory = [0] * n

    def allocate(self, size, m_id):
        run = 0
        for i in range(len(self.memory)):
            if self.memory[i] == 0:
                run += 1
                if run == size:
                    start = i + 1 - size
                    for j in range(start, i + 1):
                        self.memory[j] = m_id
                    return start
            else:
                run = 0
        return -1

    def free_memory(self, m_id):
        freed = 0
        for i in range(len(self.memory)):
            if self.memory[i] == m_id:
                self.memory[i] = 0
                freed += 1
        return freed


def drive(n, ops):
    a = Allocator(n)
    out = []
    for kind, x, y in ops:
        out.append(a.allocate(x, y) if kind == 0 else a.free_memory(x))
    return out


seed = 2502


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_ops(count, most, ids):
    # an allocate two times in three, of 1 to `most` units; else a free
    ops = []
    for _ in range(count):
        if next_random() % 3 < 2:
            ops.append((0, next_random() % most + 1, next_random() % ids + 1))
        else:
            ops.append((1, next_random() % ids + 1, 0))
    return ops


def main():
    example = [(0, 1, 1), (0, 1, 2), (0, 1, 3), (1, 2, 0), (0, 3, 4), (0, 1, 1), (0, 1, 1), (1, 1, 0), (0, 10, 2), (1, 7, 0)]
    print(f"example: {drive(10, example)}")
    print(f"one unit: {drive(1, [(0, 1, 5), (0, 1, 5), (1, 5, 0), (1, 5, 0), (0, 1, 6)])}")
    print(f"whole: {drive(4, [(0, 4, 1), (1, 1, 0), (0, 2, 2), (0, 3, 3), (0, 2, 3), (1, 2, 0), (0, 3, 1)])}")
    print(f"gaps: {drive(6, [(0, 2, 1), (0, 2, 2), (0, 2, 1), (1, 1, 0), (0, 3, 3), (0, 1, 4), (0, 2, 5), (1, 2, 0), (0, 3, 6)])}")
    for ids in [3, 20]:
        check = 0
        refused = 0
        for _ in range(2000):
            n = next_random() % 50 + 1
            for r in drive(n, random_ops(next_random() % 60 + 1, n // 3 + 1, ids)):
                if r == -1:
                    refused += 1
                check = (check * 31 + r + 1) % 1000000007
        print(f"2000 random, ids to {ids}: {refused} refused, checksum {check}")
    big = drive(1000, random_ops(1000, 20, 50))
    check = 0
    for r in big:
        check = (check * 31 + r + 1) % 1000000007
    print(f"1000 units, 1000 random calls: {big.count(-1)} refused, checksum {check}")
    ones = drive(1000, [(0, 1, i % 1000 + 1) for i in range(999)] + [(1, 500, 0)])
    print(f"1000 units, 999 of one, then a free: last {ones[-2]}, freed {ones[-1]}")


main()
