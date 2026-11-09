# LeetCode #2050: Parallel Courses III -- Python mirror of the ★ arm
# (courses.kara): Kahn's topological order, each course finished at its own
# time after the latest of its prerequisites. Output is byte-identical to
# the Kāra arms.
from collections import deque


def minimum_time(n, relations, time):
    nxt = [[] for _ in range(n)]
    waiting = [0] * n
    for a, b in relations:
        nxt[a - 1].append(b - 1)
        waiting[b - 1] += 1
    start = [0] * n
    queue = deque(v for v in range(n) if waiting[v] == 0)
    months = 0
    while queue:
        v = queue.popleft()
        done = start[v] + time[v]
        months = max(months, done)
        for w in nxt[v]:
            start[w] = max(start[w], done)
            waiting[w] -= 1
            if waiting[w] == 0:
                queue.append(w)
    return months


# ---- test harness ---------------------------------------------------------

seed = 2050


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(n, m):
    order = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        order[i], order[j] = order[j], order[i]
    m = min(m, n * (n - 1) // 2)
    seen = set()
    relations = []
    while len(relations) < m:
        a = next_random() % (n - 1)
        b = a + 1 + next_random() % (n - 1 - a)
        if (a, b) not in seen:
            seen.add((a, b))
            relations.append((order[a], order[b]))
    return relations


def times(n, most):
    return [next_random() % most + 1 for _ in range(n)]


def show(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def main():
    examples = [
        (3, [(1, 3), (2, 3)], [3, 2, 5]),
        (5, [(1, 5), (2, 5), (3, 5), (3, 4), (4, 5)], [1, 2, 3, 4, 5]),
        (1, [], [7]),
        (4, [], [4, 9, 2, 6]),
        (4, [(4, 3), (3, 2), (2, 1)], [1, 2, 3, 4]),
        (6, [(1, 2), (1, 3), (2, 4), (3, 4), (4, 5), (4, 6)], [5, 1, 8, 2, 3, 3]),
    ]
    for n, relations, time in examples:
        print(f"n {n}, {show(f'({a}, {b})' for a, b in relations)}, time {show(time)} -> {minimum_time(n, relations, time)}")
    total = check = 0
    for _ in range(2000):
        n = next_random() % 29 + 2
        m = next_random() % 61
        relations = draw(n, m)
        time = times(n, 20)
        months = minimum_time(n, relations, time)
        total += months
        check = (check * 31 + months) % 1000000007
    print(f"2000 graphs: sum {total}, checksum {check}")
    total = check = 0
    n = 50000
    chain = [(n + 1 - i, n - i) for i in range(1, n)]
    rnd = draw(n, n)
    fan = [(1, i) for i in range(2, n + 1)]
    for relations in [chain, rnd, fan]:
        time = times(n, 10000)
        months = minimum_time(n, relations, time)
        total += months
        check = (check * 31 + months) % 1000000007
    print(f"3 graphs of 50000 courses: sum {total}, checksum {check}")


main()
