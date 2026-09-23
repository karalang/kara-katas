# Benchmark mirror of LeetCode #323 — same disjoint-set forest as
# bench/count_components.kara.

NODES = 1000000
PASSES = 16
STRIDE = 9973
MODULUS = 1073741789


class DisjointSet:
    def __init__(self, n):
        self.parent = [0] * n
        self.size = [1] * n
        self.sets = n

    def reset(self):
        parent, size = self.parent, self.size
        for i in range(len(parent)):
            parent[i] = i
            size[i] = 1
        self.sets = len(parent)

    def find(self, x):
        parent = self.parent
        root = x
        while parent[root] != root:
            root = parent[root]
        cur = x
        while parent[cur] != root:
            nxt = parent[cur]
            parent[cur] = root
            cur = nxt
        return root

    def merge(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.sets -= 1


class Lcg:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536

    def draw(self, bound):
        hi = self.next()
        lo = self.next()
        return (hi * 32768 + lo) % bound


def main():
    rng = Lcg(323)
    sink = 0
    ds = DisjointSet(NODES)
    for p in range(PASSES):
        ds.reset()
        m = (1 + p % 4) * NODES // 4
        for _ in range(m):
            a = rng.draw(NODES)
            b = rng.draw(NODES)
            ds.merge(a, b)
        probe = 0
        i = 0
        while i < NODES:
            probe = (probe * 31 + ds.find(i)) % MODULUS
            i += STRIDE
        sink = (sink * 131 + ds.sets + probe) % MODULUS
    print(f"sink {sink} components {ds.sets}")


main()
