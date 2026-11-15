# LeetCode #1579 bench: the same two union-find structs, in Python.

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


seed = 1579


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    graphs = []
    for _ in range(40):
        n = 13000
        edges = []
        for u in range(1, n):
            for _ in range(next_random() % 8 + 4):
                kind = min(next_random() % 4, 2) + 1
                v = min(u + 1 + next_random() % 12, n)
                edges.append([kind, u, v])
        for i in range(len(edges) - 1, 0, -1):
            j = (next_random() * 32768 + next_random()) % (i + 1)
            edges[i], edges[j] = edges[j], edges[i]
        graphs.append((n, edges))
    check = 0
    total = 0
    stuck = 0
    for n, edges in graphs:
        removed = max_num_edges_to_remove(n, edges)
        if removed < 0:
            stuck += 1
        else:
            total += removed
        check = mix(check, removed + 1)
    print(f"40 graphs of 13000 nodes: {stuck} not traversable, edges removed {total}, checksum {check}")


main()
