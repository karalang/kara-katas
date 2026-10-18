# LeetCode 743 — Network Delay Time, Dijkstra with a priority queue.
# Mirror of network_delay_time.kara (the ★ arm); same output, byte for byte.
import heapq


def network_delay_time(times, n, k):
    adj = [[] for _ in range(n + 1)]
    for u, v, w in times:
        adj[u].append((v, w))
    heard = [-1] * (n + 1)
    queue = [(0, k)]
    settled = 0
    last = 0
    while queue:
        d, u = heapq.heappop(queue)
        if heard[u] != -1:
            continue
        heard[u] = d
        settled += 1
        last = d
        for v, w in adj[u]:
            if heard[v] == -1:
                heapq.heappush(queue, (d + w, v))
    return last if settled == n else -1


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def show(times, n, k):
    text = "[" + ", ".join(f"[{u}, {v}, {w}]" for u, v, w in times) + "]"
    print(f"{text}, n = {n}, k = {k} -> {network_delay_time(times, n, k)}")


def random_graph(rng, n, m, max_w):
    used = [False] * ((n + 1) * (n + 1))
    times = []
    while len(times) < m:
        u = 1 + rng.next() % n
        v = 1 + rng.next() % n
        if u == v or used[u * (n + 1) + v]:
            continue
        used[u * (n + 1) + v] = True
        w = rng.next() % (max_w + 1)
        times.append((u, v, w))
    return times


def twenty_sources(times, n):
    reach = 0
    total = 0
    for k in range(1, 21):
        got = network_delay_time(times, n, k)
        if got != -1:
            reach += 1
            total += got
    return reach, total


def main():
    show([(2, 1, 1), (2, 3, 1), (3, 4, 1)], 4, 2)
    show([(1, 2, 1)], 2, 1)
    show([(1, 2, 1)], 2, 2)
    show([(1, 2, 10), (1, 3, 1), (3, 2, 1)], 3, 1)
    show([(1, 2, 1), (2, 3, 2), (3, 1, 4)], 3, 2)
    show([(1, 2, 0), (2, 3, 0), (3, 1, 0)], 3, 3)
    show([(1, 2, 5), (2, 3, 5)], 4, 1)

    rng = Rng(743)
    dense = random_graph(rng, 100, 6000, 100)
    reach, total = twenty_sources(dense, 100)
    print(f"100 nodes, 6000 edges, k = 1 to 20: {reach} reach every node, answers sum to {total}")
    ring = random_graph(rng, 100, 300, 100)
    for i in range(1, 101):
        j = i % 100 + 1
        if not any(t[0] == i and t[1] == j for t in ring):
            ring.append((i, j, 100))
    reach, total = twenty_sources(ring, 100)
    print(f"a ring of 100 nodes with 300 more edges, k = 1 to 20: {reach} reach every node, answers sum to {total}")

    path = [(i, i + 1, 100) for i in range(1, 100)]
    first = network_delay_time(path, 100, 1)
    middle = network_delay_time(path, 100, 50)
    print(f"a path of 100 nodes: k = 1 -> {first}, k = 50 -> {middle}")

    reach_all = 0
    total = 0
    check = 0
    for _ in range(300):
        n = 2 + rng.next() % 7
        m = 1 + rng.next() % (n * (n - 1))
        times = random_graph(rng, n, m, 20)
        k = 1 + rng.next() % n
        got = network_delay_time(times, n, k)
        if got != -1:
            reach_all += 1
            total += got
        check = (check * 31 + got + 2) % 1000000007
    print(f"300 random graphs: {reach_all} reach every node, answers sum to {total}, checksum {check}")


main()
