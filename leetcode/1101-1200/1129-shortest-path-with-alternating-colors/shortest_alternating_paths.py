# LeetCode #1129: Shortest Path with Alternating Colors -- the Python
# mirror of the ★ arm: a breadth-first search over (node, colour of the
# edge that reached it), node 0 starting under both colours.
from collections import deque


def shortest_alternating_paths(n, red_edges, blue_edges):
    adj = [[[], []] for _ in range(n)]
    for a, b in red_edges:
        adj[a][0].append(b)
    for a, b in blue_edges:
        adj[a][1].append(b)
    dist = [[-1, -1] for _ in range(n)]
    dist[0][0] = 0
    dist[0][1] = 0
    queue = deque([(0, 0), (0, 1)])
    while queue:
        node, colour = queue.popleft()
        nxt = 1 - colour
        for m in adj[node][nxt]:
            if dist[m][nxt] < 0:
                dist[m][nxt] = dist[node][colour] + 1
                queue.append((m, nxt))
    answer = []
    for d in dist:
        a, b = d
        if a < 0:
            answer.append(b)
        elif b < 0:
            answer.append(a)
        else:
            answer.append(min(a, b))
    return answer


# ---- test harness ----

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def edges(n, m):
    return [[next_random() % n, next_random() % n] for _ in range(m)]


def main():
    global seed
    cases = [
        (3, [[0, 1], [1, 2]], []),
        (3, [[0, 1]], [[2, 1]]),
        (3, [[1, 0]], [[2, 1]]),
        (3, [[0, 1]], [[1, 2]]),
        (3, [[0, 1], [0, 2]], [[1, 0]]),
        (1, [], []),
        (5, [[0, 1], [1, 2], [2, 3], [3, 4]], [[1, 2], [2, 3], [3, 1]]),
        (4, [[0, 0], [0, 1]], [[0, 0], [1, 2], [2, 3]]),
        (6, [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]], [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]]),
    ]
    for n, r, b in cases:
        print(f"n = {n}, red {r}, blue {b} -> {shortest_alternating_paths(n, r, b)}".replace("'", ""))
    seed = 1129
    total = 0
    reached = 0
    check = 0
    for t in range(2000):
        n = next_random() % 100 + 1
        r = edges(n, next_random() % (2 * n + 1))
        b = edges(n, next_random() % (2 * n + 1))
        answer = shortest_alternating_paths(n, r, b)
        for d in answer:
            total += d
            if d >= 0:
                reached += 1
            check = (check * 31 + d + 2) % 1000000007
    print(f"2000 random graphs: {reached} nodes reached, lengths total {total}, checksum {check}")
    r = edges(100, 400)
    b = edges(100, 400)
    big = shortest_alternating_paths(100, r, b)
    print(f"100 nodes, 400 edges of each colour: {sum(1 for d in big if d >= 0)} reached, longest {max(big)}")
    chain_r = [[i, i + 1] for i in range(0, 99, 2)]
    chain_b = [[i, i + 1] for i in range(1, 99, 2)]
    chain = shortest_alternating_paths(100, chain_r, chain_b)
    print(f"an alternating chain of 100: last {chain[99]}, total {sum(chain)}")


main()
