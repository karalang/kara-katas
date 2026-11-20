# LeetCode #1743: Restore the Array From Adjacent Pairs -- the bench
# (restore.kara in Python): the pairs as a graph, walked from an end.


def restore_array(adjacent_pairs):
    near = {}
    for a, b in adjacent_pairs:
        near.setdefault(a, []).append(b)
        near.setdefault(b, []).append(a)
    start = next(v for v, n in near.items() if len(n) == 1)
    order = [start, near[start][0]]
    while len(order) < len(adjacent_pairs) + 1:
        before, last = order[-2], order[-1]
        n = near[last]
        order.append(n[1] if n[0] == before else n[0])
    return order


seed = 1743


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    return next_random() * 32768 + next_random()


def random_pairs(n):
    taken = set()
    values = []
    while len(values) < n:
        v = wide() % 200001 - 100000
        if v not in taken:
            taken.add(v)
            values.append(v)
    pairs = []
    for i in range(1, n):
        if next_random() % 2 == 0:
            pairs.append([values[i - 1], values[i]])
        else:
            pairs.append([values[i], values[i - 1]])
    for i in range(len(pairs) - 1, 0, -1):
        j = next_random() % (i + 1)
        pairs[i], pairs[j] = pairs[j], pairs[i]
    return pairs


count, rounds, n = 10, 4, 100000
problems = [random_pairs(n) for _ in range(count)]
total = 0
check = 0
for r in range(rounds):
    for pairs in problems:
        order = restore_array(pairs)
        first, last = order[0], order[-1]
        middle = order[len(order) // 2] if first < last else order[len(order) - 1 - len(order) // 2]
        low = min(first, last)
        total += low
        check = (check * 31 + low + middle + 200000 + r) % 1000000007
print(f"{count} arrays of {n} values, {rounds} rounds: smaller ends sum to {total}, checksum {check}")
