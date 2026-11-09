# LeetCode #2039: The Time When the Network Becomes Idle -- the ★ arm in
# Python, the same algorithm and workload as network.kara: breadth-first
# search from the master with a deque, then each server's last message and
# its reply.
from collections import deque


def network_becomes_idle(edges, patience):
    n = len(patience)
    adjacent = [[] for _ in range(n)]
    for u, v in edges:
        adjacent[u].append(v)
        adjacent[v].append(u)
    hops = [-1] * n
    hops[0] = 0
    queue = deque([0])
    while queue:
        u = queue.popleft()
        for v in adjacent[u]:
            if hops[v] == -1:
                hops[v] = hops[u] + 1
                queue.append(v)
    idle = 0
    for i in range(1, n):
        round_trip = 2 * hops[i]
        last_sent = (round_trip - 1) // patience[i] * patience[i]
        idle = max(idle, last_sent + round_trip + 1)
    return idle


seed = 2039


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_network(n, reach, extra, top):
    edges = []
    joined = set()
    for v in range(1, n):
        u = v - 1 - (next_random() * 32768 + next_random()) % min(reach, v)
        edges.append([u, v])
        joined.add((u, v))
    tries = 0
    while len(edges) < n - 1 + extra and tries < 4 * extra:
        tries += 1
        a = (next_random() * 32768 + next_random()) % n
        b = (next_random() * 32768 + next_random()) % n
        u, v = min(a, b), max(a, b)
        if u != v and (u, v) not in joined:
            joined.add((u, v))
            edges.append([u, v])
    patience = [0]
    for _ in range(1, n):
        patience.append(next_random() % top + 1)
    return edges, patience


def main():
    networks = []
    for r in range(4):
        top = [100000, 3, 1000, 1][r]
        reach = [100000, 2, 50, 1][r]
        networks.append(random_network(100000, reach, 1, top))
    calls = 0
    total = 0
    check = 0
    for rnd in range(25):
        for r in range(4):
            at = (rnd * 7919 + r * 104729) % 99999 + 1
            edges, patience = networks[r]
            patience[at] = patience[at] % 7 + 1
            answer = network_becomes_idle(edges, patience)
            calls += 1
            total += answer
            check = (check * 31 + answer) % 1000000007
    print(f"{calls} calls: sum {total}, checksum {check}")


main()
