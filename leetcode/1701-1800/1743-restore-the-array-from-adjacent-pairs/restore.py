# LeetCode #1743: Restore the Array From Adjacent Pairs -- mirrors
# restore.kara (the ★ arm).


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


def canonical(order):
    return order[::-1] if order[0] > order[-1] else order


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


def batch(count, most):
    total = 0
    check = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % (most - 1) + 2
        order = canonical(restore_array(random_pairs(n)))
        for v in order:
            check = (check * 31 + v + 100000) % 1000000007
        total += order[0]
    print(f"{count} arrays of up to {most} values: first values sum to {total}, checksum {check}")


def show(order):
    return "[" + ", ".join(map(str, order)) + "]"


print(show(canonical(restore_array([[2, 1], [3, 4], [3, 2]]))))
print(show(canonical(restore_array([[4, -2], [1, 4], [-3, 1]]))))
print(show(canonical(restore_array([[100000, -100000]]))))
print(show(canonical(restore_array([[3, 2], [2, 1]]))))
batch(3000, 8)
batch(300, 1000)
batch(10, 100000)
