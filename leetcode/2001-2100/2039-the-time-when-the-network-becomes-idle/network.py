# LeetCode #2039: The Time When the Network Becomes Idle -- the ★ arm in
# Python, the same algorithm and harness as network.kara: breadth-first
# search from the master, then each server's last message and its reply.
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


def mix(check, answer):
    return (check * 31 + answer) % 1000000007


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


def show(v):
    if isinstance(v, list):
        return "[" + ", ".join(show(x) for x in v) + "]"
    return str(v)


def main():
    examples = [
        ([[0, 1], [1, 2]], [0, 2, 1]),
        ([[0, 1], [0, 2], [1, 2]], [0, 10, 10]),
        ([[0, 1]], [0, 1]),
        ([[0, 1]], [0, 5]),
        ([[0, 1], [1, 2], [2, 3], [3, 4]], [0, 1, 3, 7, 100000]),
        ([[3, 0], [2, 3], [1, 2], [0, 1]], [0, 4, 3, 2]),
    ]
    for edges, patience in examples:
        print(f"{show(edges)} {show(patience)} -> {network_becomes_idle(edges, patience)}")
    total = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 11 + 2
        extra = next_random() % (n + 1)
        top = next_random() % 10 + 1
        edges, patience = random_network(n, n, extra, top)
        answer = network_becomes_idle(edges, patience)
        total += answer
        check = mix(check, answer)
    print(f"2000 networks of up to 12 servers: sum {total}, checksum {check}")
    total = 0
    check = 0
    for r in range(4):
        top = [100000, 3, 1000, 1][r]
        reach = [100000, 2, 50, 1][r]
        edges, patience = random_network(100000, reach, 1, top)
        answer = network_becomes_idle(edges, patience)
        total += answer
        check = mix(check, answer)
    print(f"4 networks of 100000 servers: sum {total}, checksum {check}")


main()
