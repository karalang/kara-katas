# LeetCode #1129: Shortest Path with Alternating Colors -- the bench in
# Python, the ★ arm over lists of two-number lists: the adjacency built per
# call as one list per node and colour, a breadth-first search over (node,
# colour) with a deque, the same 32 graphs and 1000 rounds.
from collections import deque


def shortest_alternating_paths(n, red_edges, blue_edges):
    adj = [[[] for _ in range(n)] for _ in range(2)]
    for e in red_edges:
        adj[0][e[0]].append(e[1])
    for e in blue_edges:
        adj[1][e[0]].append(e[1])
    dist = [[-1] * n for _ in range(2)]
    dist[0][0] = 0
    dist[1][0] = 0
    queue = deque([(0, 0), (0, 1)])
    while queue:
        node, colour = queue.popleft()
        nxt = 1 - colour
        for m in adj[nxt][node]:
            if dist[nxt][m] < 0:
                dist[nxt][m] = dist[colour][node] + 1
                queue.append((m, nxt))
    out = []
    for x in range(n):
        a, b = dist[0][x], dist[1][x]
        out.append(b if a < 0 else a if b < 0 else min(a, b))
    return out


seed = 1129


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def edges(n, m):
    out = []
    for _ in range(m):
        a = next_random() % n
        b = next_random() % n
        out.append([a, b])
    return out


def main():
    reds, blues = [], []
    for _ in range(32):
        reds.append(edges(100, 400))
        blues.append(edges(100, 400))
    total = 0
    check = 0
    for rnd in range(1000):
        for j in range(32):
            at = (rnd * 7919 + j * 104729) % 400
            e = reds[j] if rnd % 2 == 0 else blues[j]
            e[at][1] = (e[at][1] + 1 + rnd % 7) % 100
            for d in shortest_alternating_paths(100, reds[j], blues[j]):
                total += d
                check = (check * 31 + d + 2) % 1000000007
    print(f"1000 rounds over 32 graphs of 100 nodes and 400 edges of each colour: lengths total {total}, checksum {check}")


main()
