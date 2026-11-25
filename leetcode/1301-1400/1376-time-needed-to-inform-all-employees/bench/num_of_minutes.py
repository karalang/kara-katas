# LeetCode #1376 bench -- Python: the ★ arm: each manager's reports in a
# list, then a breadth-first walk down from the head, each employee
# hearing the news when the manager heard it plus the manager's inform
# time.

from collections import deque


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
        if heard[u] > latest:
            latest = heard[u]
        for v in reports[u]:
            heard[v] = heard[u] + inform_time[u]
            queue.append(v)
    return latest


seed = 1376


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 10 companies of 10^5 employees, built once; then 200 rounds, each
    # giving one employee of one company a new inform time if it is a
    # manager, and timing that company (see the Kāra bench)
    n = 100000
    heads, managers, informs = [], [], []
    for _ in range(10):
        order = list(range(n))
        for i in range(n - 1, 0, -1):
            j = next_random() % (i + 1)
            order[i], order[j] = order[j], order[i]
        manager = [-1] * n
        inform = [0] * n
        for k in range(1, n):
            m = order[next_random() % k]
            manager[order[k]] = m
            if inform[m] == 0:
                inform[m] = 1 + next_random() % 1000
        heads.append(order[0])
        managers.append(manager)
        informs.append(inform)
    check = 0
    for r in range(200):
        c = check % 10
        e = (check // 10) % n
        if informs[c][e] > 0:
            informs[c][e] = 1 + (check + r) % 1000
        got = num_of_minutes(n, heads[c], managers[c], informs[c])
        check = (check * 31 + got + r) % 1000000007
    print(f"200 rounds over 10 companies of 100000 employees: checksum {check}")


main()
