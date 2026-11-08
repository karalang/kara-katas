# LeetCode #1514: Path with Maximum Probability -- the bench: 10 graphs of
# 50000 nodes and 100000 edges built once, then 5 questions asked of each
# by the ★ arm.
import heapq
import math


def max_probability(n, edges, succ_prob, start, end):
    adjacent = [[] for _ in range(n)]
    for (a, b), p in zip(edges, succ_prob):
        adjacent[a].append((b, p))
        adjacent[b].append((a, p))
    best = [0.0] * n
    best[start] = 1.0
    queue = [(-1.0, start)]
    while queue:
        neg, node = heapq.heappop(queue)
        chance = -neg
        if node == end:
            return chance
        if chance < best[node]:
            continue
        for nxt, p in adjacent[node]:
            through = chance * p
            if through > best[nxt]:
                best[nxt] = through
                heapq.heappush(queue, (-through, nxt))
    return 0.0


seed = 1514


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    hi = next_random() * 32768
    return hi + next_random()


n = 50000
graphs = []
for _ in range(10):
    edges, probs = [], []
    for _ in range(100000):
        a = wide() % n
        b = (a + 1 + wide() % (n - 1)) % n
        edges.append((a, b))
        probs.append((next_random() % 21 + 80) / 100.0)
    graphs.append((edges, probs))
check = 0
for _ in range(5):
    for edges, probs in graphs:
        start = wide() % n
        end = wide() % n
        p = max_probability(n, edges, probs, start, end)
        check = (check * 31 + math.floor(p * 1000000000000.0 + 0.5) + 1) % 1000000007
print(f"50 questions over 10 graphs of 50000 nodes: checksum {check}")
