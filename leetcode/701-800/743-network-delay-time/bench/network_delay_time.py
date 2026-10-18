# LeetCode 743 — Network Delay Time, bench: the ★ arm (Dijkstra with a
# priority queue) on a 100-node graph of 6000 edges, every source, while
# edge times change. Mirrors network_delay_time.kara.
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


seed = 743


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_graph(n, m, max_w):
    used = [False] * ((n + 1) * (n + 1))
    times = []
    while len(times) < m:
        u = 1 + next_random() % n
        v = 1 + next_random() % n
        if u == v or used[u * (n + 1) + v]:
            continue
        used[u * (n + 1) + v] = True
        w = next_random() % (max_w + 1)
        times.append((u, v, w))
    return times


def main():
    rounds = 12
    times = random_graph(100, 6000, 100)
    total = 0
    for _ in range(rounds):
        for _ in range(50):
            i = next_random() % len(times)
            w = next_random() % 101
            u, v, _ = times[i]
            times[i] = (u, v, w)
        for k in range(1, 101):
            total += network_delay_time(times, 100, k)
    print(f"{rounds} rounds of 100 queries on 100 nodes and 6000 edges: answers sum to {total}")


main()
