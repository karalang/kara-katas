# LeetCode #1579: Remove Max Number of Edges to Keep Graph Fully Traversable
# -- the Python mirror of the ★ arm: two disjoint-set forests with path
# halving and union by size; the type 3 edges go into both first, then
# type 1 into Alice's and type 2 into Bob's. O(m α(n))


class Dsu:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.size = [1] * (n + 1)
        self.parts = n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def join(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        big, small = (rb, ra) if self.size[ra] < self.size[rb] else (ra, rb)
        self.parent[small] = big
        self.size[big] += self.size[small]
        self.parts -= 1
        return True


def max_num_edges_to_remove(n, edges):
    alice = Dsu(n)
    bob = Dsu(n)
    kept = 0
    for e in edges:
        if e[0] == 3:
            a = alice.join(e[1], e[2])
            b = bob.join(e[1], e[2])
            if a or b:
                kept += 1
    for e in edges:
        if e[0] == 1 and alice.join(e[1], e[2]):
            kept += 1
        if e[0] == 2 and bob.join(e[1], e[2]):
            kept += 1
    if alice.parts != 1 or bob.parts != 1:
        return -1
    return len(edges) - kept


# ---- the harness: the same in every arm

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, draws, reach):
    check = 0
    total = 0
    stuck = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % most + 2
        seen = set()
        edges = []
        for u in range(1, n):
            for _ in range(next_random() % draws + 1):
                kind = min(next_random() % 4, 2) + 1
                v = min(u + 1 + next_random() % reach, n)
                key = (kind * (n + 1) + u) * (n + 1) + v
                if key not in seen:
                    seen.add(key)
                    edges.append([kind, u, v])
        for i in range(len(edges) - 1, 0, -1):
            j = (next_random() * 32768 + next_random()) % (i + 1)
            edges[i], edges[j] = edges[j], edges[i]
        removed = max_num_edges_to_remove(n, edges)
        if removed < 0:
            stuck += 1
        else:
            total += removed
        check = mix(check, removed + 1)
    print(f"{count} graphs of up to {most + 1} nodes: {stuck} not traversable, edges removed {total}, checksum {check}")


def show(edges):
    return "[" + ", ".join("[" + ", ".join(str(x) for x in e) + "]" for e in edges) + "]"


def main():
    global seed
    examples = [
        (4, [[3, 1, 2], [3, 2, 3], [1, 1, 3], [1, 2, 4], [1, 1, 2], [2, 3, 4]]),
        (4, [[3, 1, 2], [3, 2, 3], [1, 1, 4], [2, 1, 4]]),
        (4, [[3, 2, 3], [1, 1, 2], [2, 3, 4]]),
        (2, [[1, 1, 2], [2, 1, 2], [3, 1, 2]]),
        (3, [[3, 1, 2], [3, 2, 3], [3, 1, 3], [1, 1, 3], [2, 1, 2]]),
        (3, [[1, 1, 2], [1, 2, 3], [2, 1, 3]]),
    ]
    for n, edges in examples:
        print(f"{n} {show(edges)} -> {max_num_edges_to_remove(n, edges)}")
    seed = 1579
    batch(3000, 5, 3, 2)
    batch(300, 300, 8, 8)
    batch(10, 10000, 14, 12)


main()
