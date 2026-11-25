# LeetCode #1376: Time Needed to Inform All Employees -- Python mirror of
# the ★ arm: each manager's reports in a list, then a breadth-first walk
# down from the head, each employee hearing the news when the manager
# heard it plus the manager's inform time.

from collections import deque

seed = 1376


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def num_of_minutes(n, head_id, manager, inform_time):
    reports = [[] for _ in range(n)]
    for i, m in enumerate(manager):
        if m >= 0:
            reports[m].append(i)
    heard = [0] * n
    queue = deque([head_id])
    latest = 0
    while queue:
        u = queue.popleft()
        latest = max(latest, heard[u])
        for v in reports[u]:
            heard[v] = heard[u] + inform_time[u]
            queue.append(v)
    return latest


def company(n, kind):
    order = list(range(n))
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        order[i], order[j] = order[j], order[i]
    manager = [-1] * n
    inform = [0] * n
    for k in range(1, n):
        if kind == 0:
            back = next_random() % k
        elif kind == 1:
            back = k - 1 - next_random() % min(k, 3)
        elif kind == 2:
            back = next_random() % min(k, 3)
        else:
            back = k // 2 + next_random() % (k - k // 2)
        manager[order[k]] = order[back]
    for i in range(n):
        if manager[i] >= 0:
            m = manager[i]
            if inform[m] == 0:
                inform[m] = 1 + next_random() % 1000 if kind % 2 == 0 else 1 + next_random() % 5
    return order[0], manager, inform


def main():
    n = 100000
    shown = [
        num_of_minutes(1, 0, [-1], [0]),
        num_of_minutes(6, 2, [2, 2, -1, 2, 2, 2], [0, 0, 1, 0, 0, 0]),
        num_of_minutes(n, 0, [i - 1 for i in range(n)], [0 if i == n - 1 else 1000 for i in range(n)]),
        num_of_minutes(n, n - 1, [-1 if i == n - 1 else i + 1 for i in range(n)], [0 if i == 0 else 1 + i % 1000 for i in range(n)]),
        num_of_minutes(n, 0, [-1 if i == 0 else 0 for i in range(n)], [1000 if i == 0 else 0 for i in range(n)]),
        num_of_minutes(n, 0, [-1 if i == 0 else (i - 1) // 2 for i in range(n)], [1 + i * 7 % 1000 if 2 * i + 1 < n else 0 for i in range(n)]),
    ]
    print(" ".join(str(x) for x in shown))
    total = 0
    check = 0
    for c in range(2000):
        n = 1 + next_random() % 300
        head, manager, inform = company(n, c % 4)
        got = num_of_minutes(n, head, manager, inform)
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random companies: {total} minutes in all, checksum {check}")


main()
