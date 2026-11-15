# LeetCode #1168 mirror of the Kāra ★ arm: Kruskal over the pipes and one
# pipe from a well node 0 to every house, union-find by size with halving.
import sys

def min_cost(n, wells, pipes):
    edges = [(w, 0, i + 1) for i, w in enumerate(wells)] + [(c, a, b) for a, b, c in pipes]
    edges.sort()
    parent = list(range(n + 1)); size = [1] * (n + 1)
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    cost = 0; joined = 0
    for c, a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb: continue
        if size[ra] < size[rb]: ra, rb = rb, ra
        parent[rb] = ra; size[ra] += size[rb]; cost += c; joined += 1
        if joined == n: break
    return cost

def literal(n, wells, pipes):
    best = None
    p = len(pipes)
    for wm in range(1 << n):
        wc = sum(wells[i] for i in range(n) if wm >> i & 1)
        if best is not None and wc >= best: continue
        for pm in range(1 << p):
            c = wc + sum(pipes[j][2] for j in range(p) if pm >> j & 1)
            if best is not None and c >= best: continue
            water = [wm >> i & 1 == 1 for i in range(n)]
            changed = True
            while changed:
                changed = False
                for j in range(p):
                    if pm >> j & 1:
                        a, b = pipes[j][0] - 1, pipes[j][1] - 1
                        if water[a] != water[b]:
                            water[a] = water[b] = True; changed = True
            if all(water): best = c
    return best

state = [1168]
def rnd():
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536

F = literal if len(sys.argv) > 1 and sys.argv[1] == 'lit' else min_cost

def show(n, wells, pipes):
    print(f"{n} {wells} {pipes} -> {F(n, wells, pipes)}")

show(3, [1, 2, 2], [[1, 2, 1], [2, 3, 1]])
show(2, [1, 1], [[1, 2, 1], [1, 2, 2]])
show(2, [1, 1], [[1, 2, 1]])
show(3, [5, 5, 5], [[1, 2, 9], [2, 3, 9]])
show(4, [9, 1, 9, 9], [[1, 2, 2], [2, 3, 2], [3, 4, 2], [1, 4, 1]])
show(3, [0, 4, 4], [[1, 2, 0], [2, 3, 3], [1, 3, 5]])
show(5, [7, 7, 7, 7, 7], [[1, 2, 3], [2, 3, 3], [4, 5, 3]])
total = 0; check = 0
for i in range(300):
    n = 2 + rnd() % 29
    small = i % 2 == 0
    top = 10 if small else 100000
    wells = [rnd() % (top + 1) for _ in range(n)]
    m = 1 + rnd() % (2 * n)
    pipes = []
    for _ in range(m):
        a = 1 + rnd() % n; b = 1 + rnd() % (n - 1)
        if b >= a: b += 1
        pipes.append([a, b, rnd() % (top + 1)])
    if F is literal and (n > 5 or m > 6):
        c = min_cost(n, wells, pipes)
    else:
        c = F(n, wells, pipes)
    total += c; check = (check * 31 + c) % 1000000007
print(f"300 random villages: total {total}, checksum {check}")
n = 10000
wells = [rnd() % 100001 for _ in range(n)]
pipes = []
for _ in range(10000):
    a = 1 + rnd() % n; b = 1 + rnd() % (n - 1)
    if b >= a: b += 1
    pipes.append([a, b, rnd() % 100001])
print(f"10000 houses, 10000 random pipes: {min_cost(n, wells, pipes)}")
pipes = [[i, i + 1, 1] for i in range(1, n)] + [[1, n, 0]]
print(f"10000 houses in a ring of cheap pipes: {min_cost(n, [100000] * n, pipes)}")
