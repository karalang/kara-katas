# LeetCode #1203: Sort Items by Groups Respecting Dependencies -- the ★ arm
# in Python: each item with no group given a group of its own, then two
# topological sorts by Kahn's algorithm, one of the groups and one of the
# items; the items, in their sorted order, dealt into their groups, and the
# groups laid out in theirs.


def topo_sort(nodes, edges):
    indegree = [0] * nodes
    for out in edges:
        for v in out:
            indegree[v] += 1
    order = [v for v in range(nodes) if indegree[v] == 0]
    head = 0
    while head < len(order):
        u = order[head]
        head += 1
        for v in edges[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                order.append(v)
    return order if len(order) == nodes else []


def sort_items(n, m, group, before_items):
    group = list(group)
    groups = m
    for i in range(n):
        if group[i] < 0:
            group[i] = groups
            groups += 1
    item_edges = [[] for _ in range(n)]
    group_edges = [[] for _ in range(groups)]
    for i in range(n):
        for b in before_items[i]:
            item_edges[b].append(i)
            if group[b] != group[i]:
                group_edges[group[b]].append(group[i])
    items = topo_sort(n, item_edges)
    ranks = topo_sort(groups, group_edges)
    if not items or not ranks:
        return []
    members = [[] for _ in range(groups)]
    for i in items:
        members[group[i]].append(i)
    out = []
    for g in ranks:
        out.extend(members[g])
    return out


# ---- test harness ---------------------------------------------------------


def valid(n, group, before_items, order):
    if len(order) != n:
        return False
    at = [-1] * n
    for k, i in enumerate(order):
        if i < 0 or i >= n or at[i] >= 0:
            return False
        at[i] = k
    for i in range(n):
        for b in before_items[i]:
            if at[b] > at[i]:
                return False
    closed = set()
    for k in range(1, n):
        prev, g = group[order[k - 1]], group[order[k]]
        if prev != g:
            if g >= 0 and g in closed:
                return False
            closed.add(prev)
    return True


def report(n, m, group, before_items):
    order = sort_items(n, m, group, before_items)
    if not order:
        return "none"
    if valid(n, group, before_items, order):
        return f"an order of {n}"
    return f"INVALID {order}"


seed = 1203


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return "[" + ", ".join(show(x) if isinstance(x, list) else str(x) for x in v) + "]"


def main():
    cases = [
        (8, 2, [-1, -1, 1, 0, 0, 1, 0, -1], [[], [6], [5], [6], [3, 6], [], [], []]),
        (8, 2, [-1, -1, 1, 0, 0, 1, 0, -1], [[], [6], [5], [6], [3], [], [4], []]),
        (1, 1, [-1], [[]]),
        (3, 1, [0, -1, 0], [[], [0], [1]]),
        (3, 1, [0, -1, 0], [[], [], [1]]),
        (4, 2, [0, 1, 0, 1], [[], [], [1], [2]]),
        (4, 2, [0, 1, 0, 1], [[1], [], [], [2]]),
        (5, 3, [-1, -1, -1, -1, -1], [[1], [2], [3], [4], []]),
        (2, 1, [-1, -1], [[1], [0]]),
    ]
    for n, m, group, before_items in cases:
        print(f"{n} {m} {show(group)} {show(before_items)}: {report(n, m, group, before_items)}")
    ordered = none = wrong = 0
    for _ in range(1000):
        n = next_random() % 9 + 1
        m = next_random() % n + 1
        group = [next_random() % (m + 1) - 1 for _ in range(n)]
        before_items = [[] for _ in range(n)]
        for i in range(n):
            for _ in range(next_random() % 3):
                b = next_random() % n
                if b != i and b not in before_items[i]:
                    before_items[i].append(b)
        r = report(n, m, group, before_items)
        if r == "none":
            none += 1
        elif r.startswith("an order"):
            ordered += 1
        else:
            wrong += 1
    print(f"1000 random cases: {ordered} ordered, {none} with none, {wrong} invalid")
    n, m = 30000, 3000
    group = [-1 if i % 3 == 0 else i // 10 for i in range(n)]
    before_items = [[] for _ in range(n)]
    for i in range(1, n):
        for _ in range(next_random() % 4):
            hi = next_random()
            b = (hi * 32768 + next_random()) % i
            if b not in before_items[i]:
                before_items[i].append(b)
    print(f"30000 items, 3000 groups: {report(n, m, group, before_items)}")
    before_items[0].append(n - 1)
    before_items[n - 1].append(0)
    print(f"30000 items, one cycle: {report(n, m, group, before_items)}")


main()
