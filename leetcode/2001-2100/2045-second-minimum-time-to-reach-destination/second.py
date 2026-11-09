# LeetCode #2045: Second Minimum Time to Reach Destination -- Python mirror
# of the ★ arm (second.kara): a breadth-first search keeping each vertex's
# two smallest distinct walk lengths, then the lights applied to the second
# one at `n`.
from collections import deque


def travel(steps, time, change):
    t = 0
    for _ in range(steps):
        if t // change % 2 == 1:
            t = (t // change + 1) * change
        t += time
    return t


def second_minimum(n, edges, time, change):
    adjacent = [[] for _ in range(n + 1)]
    for u, v in edges:
        adjacent[u].append(v)
        adjacent[v].append(u)
    first = [-1] * (n + 1)
    second = [-1] * (n + 1)
    first[1] = 0
    queue = deque([(1, 0)])
    while queue:
        u, d = queue.popleft()
        for v in adjacent[u]:
            if first[v] == -1:
                first[v] = d + 1
                queue.append((v, d + 1))
            elif second[v] == -1 and first[v] < d + 1:
                second[v] = d + 1
                queue.append((v, d + 1))
    return travel(second[n], time, change)


# ---- test harness ---------------------------------------------------------

seed = 2045


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def graph(n, reach, extra):
    edges = []
    seen = set()
    for v in range(2, n + 1):
        u = v - 1 - next_random() % min(reach, v - 1)
        edges.append([u, v])
        seen.add(u * (n + 1) + v)
    tries = 0
    while len(edges) < n - 1 + extra and tries < 4 * extra:
        tries += 1
        a = next_random() % n + 1
        b = next_random() % n + 1
        u, v = min(a, b), max(a, b)
        if u != v and u * (n + 1) + v not in seen:
            seen.add(u * (n + 1) + v)
            edges.append([u, v])
    return edges


def show(edges):
    return "[" + ", ".join(f"[{u}, {v}]" for u, v in edges) + "]"


def main():
    examples = [
        (5, [[1, 2], [1, 3], [1, 4], [3, 4], [4, 5]], 3, 5),
        (2, [[1, 2]], 3, 2),
        (3, [[1, 2], [2, 3], [1, 3]], 1, 1),
        (4, [[1, 2], [2, 3], [3, 4]], 1000, 1),
        (4, [[1, 2], [2, 3], [3, 4]], 1, 1000),
        (3, [[1, 2], [1, 3]], 2, 3),
    ]
    for n, edges, time, change in examples:
        print(f"{n} {show(edges)} {time} {change} -> {second_minimum(n, edges, time, change)}")
    total = check = 0
    for _ in range(2000):
        n = next_random() % 9 + 2
        reach = next_random() % n + 1
        extra = next_random() % (n + 1)
        edges = graph(n, reach, extra)
        time = next_random() % 10 + 1
        change = next_random() % 10 + 1
        answer = second_minimum(n, edges, time, change)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"2000 small graphs: sum {total}, checksum {check}")
    total = check = 0
    for r in range(4):
        reach = [10000, 3, 2, 1][r]
        edges = graph(10000, reach, 10001)
        time = [1000, 7, 1, 1000][r]
        change = [1000, 3, 1000, 1][r]
        answer = second_minimum(10000, edges, time, change)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"4 large graphs: sum {total}, checksum {check}")


main()
