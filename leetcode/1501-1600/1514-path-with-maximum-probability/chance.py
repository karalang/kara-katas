# LeetCode #1514: Path with Maximum Probability -- the Python mirror of the
# ★ arm: Dijkstra for the largest product, a largest-first queue (heapq on
# the negated chance).
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


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def fixed(p):
    return math.floor(p * 100000.0 + 0.5)


def batch(count, most, spread):
    check = 0
    for _ in range(count):
        n = next_random() % (most - 1) + 2
        m = next_random() % (spread * n) + 1
        edges, probs = [], []
        for _ in range(m):
            a = next_random() % n
            b = (a + 1 + next_random() % (n - 1)) % n
            edges.append((a, b))
            probs.append((next_random() % 21 + 80) / 100.0)
        start = next_random() % n
        end = (start + 1 + next_random() % (n - 1)) % n
        check = mix(check, fixed(max_probability(n, edges, probs, start, end)))
    return check


edges = [(0, 1), (1, 2), (0, 2)]
print(f"example 1 -> {max_probability(3, edges, [0.5, 0.5, 0.2], 0, 2):.5f}")
print(f"example 2 -> {max_probability(3, edges, [0.5, 0.5, 0.3], 0, 2):.5f}")
print(f"example 3 -> {max_probability(3, [(0, 1)], [0.5], 0, 2):.5f}")
chain = [(i, i + 1) for i in range(9)]
print(f"a chain of ten at 0.9 -> {max_probability(10, chain, [0.9] * 9, 0, 9):.5f}")
print(f"2000 graphs of 2 to 8 nodes: checksum {batch(2000, 8, 2)}")
print(f"200 graphs of 2 to 200 nodes: checksum {batch(200, 200, 2)}")
print(f"3 graphs of 2 to 10000 nodes: checksum {batch(3, 10000, 2)}")
