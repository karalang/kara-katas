# LeetCode #1238: Circular Permutation in Binary Representation -- Python
# mirror of the ★ arm: the reflected Gray code moved to `start` by XOR.


def circular_permutation(n, start):
    return [start ^ i ^ (i >> 1) for i in range(1 << n)]


# ---- test harness ---------------------------------------------------------

def is_cycle(n, start, p):
    size = 1 << n
    if len(p) != size or p[0] != start:
        return False
    seen = [False] * size
    for v in p:
        if v < 0 or v >= size or seen[v]:
            return False
        seen[v] = True
    for i in range(size):
        d = p[i] ^ p[(i + 1) % size]
        if not (d != 0 and d & (d - 1) == 0):
            return False
    return True


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def main():
    for n, start in [(2, 3), (3, 2)]:
        p = circular_permutation(n, start)
        print(f"n = {n}, start = {start}: {len(p)} values, a cycle: {'true' if is_cycle(n, start, p) else 'false'}")
    rng = Rng(1238)
    cycles = 0
    values = 0
    for _ in range(1000):
        n = rng.next() % 12 + 1
        start = rng.next() % (1 << n)
        p = circular_permutation(n, start)
        values += len(p)
        if is_cycle(n, start, p):
            cycles += 1
    print(f"1000 random cases: {cycles} cycles, {values} values")
    top = sum(1 for start in [0, 40000, 65535] if is_cycle(16, start, circular_permutation(16, start)))
    print(f"n = 16: {top} of 3 cycles of 65536")


main()
