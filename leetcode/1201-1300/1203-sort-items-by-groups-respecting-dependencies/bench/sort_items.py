# LeetCode #1203 bench, in Python: the ★ arm (each item in no group given
# one of its own, then Kahn's algorithm over the groups and over the items)
# on four instances of 30000 items drawn once, then 10 rounds over the
# four, each answer folded into a checksum.

seed = 1203


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


def dependencies(n, most):
    before_items = [[] for _ in range(n)]
    for i in range(1, n):
        for _ in range(next_random() % (most + 1)):
            hi = next_random()
            b = (hi * 32768 + next_random()) % i
            if b not in before_items[i]:
                before_items[i].append(b)
    return before_items


def main():
    n, m = 30000, 3000
    runs = [-1 if i % 10 == 0 else i // 10 for i in range(n)]
    loose = dependencies(n, 3)
    dense = dependencies(n, 6)
    cycle = [list(b) for b in loose]
    cycle[0].append(n - 1)
    if 0 not in cycle[n - 1]:
        cycle[n - 1].append(0)
    instances = [(runs, loose), (runs, dense), ([-1] * n, dependencies(n, 3)), (runs, cycle)]
    check = 0
    for _ in range(10):
        for group, before_items in instances:
            order = sort_items(n, m, group, before_items)
            check = (check * 131 + len(order)) % 1000000007
            for i in order:
                check = (check * 131 + i + 1) % 1000000007
    print(f"10 rounds over 4 instances of 30000 items: checksum {check}")


main()
