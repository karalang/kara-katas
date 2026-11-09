# LeetCode #2050: Parallel Courses III -- Python mirror of the ★ arm's
# benchmark (courses.kara): the same 40 graphs of 50000 courses, the same
# Kahn's topological order.
from collections import deque

seed = 2050


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


def main():
    n = 50000
    total = check = 0
    for t in range(40):
        reach = 1 + t * 1000
        order = list(range(1, n + 1))
        for i in range(n - 1, 0, -1):
            j = next_random() % (i + 1)
            order[i], order[j] = order[j], order[i]
        relations = []
        for i in range(1, n):
            at = i - (next_random() % min(reach, i) + 1)
            relations.append((order[at], order[i]))
        time = [next_random() % 10000 + 1 for _ in range(n)]
        months = minimum_time(n, relations, time)
        total += months
        check = (check * 31 + months) % 1000000007
    print(f"40 graphs: sum {total}, checksum {check}")


main()
