# LeetCode #2049: Count Nodes With the Highest Score -- Python mirror of the
# ★ arm (highest.kara): a preorder by an explicit stack, sizes summed
# walking it backwards, each node's score the product of its parts. Output
# is byte-identical to the Kāra arms.


def count_highest_score_nodes(parents):
    n = len(parents)
    children = [[] for _ in range(n)]
    root = 0
    for v in range(n):
        if parents[v] == -1:
            root = v
        else:
            children[parents[v]].append(v)
    order = []
    stack = [root]
    while stack:
        v = stack.pop()
        order.append(v)
        for c in children[v]:
            stack.append(c)
    size = [1] * n
    for v in reversed(order):
        if parents[v] != -1:
            size[parents[v]] += size[v]
    best = count = 0
    for v in range(n):
        score = max(n - size[v], 1)
        for c in children[v]:
            score *= size[c]
        if score > best:
            best, count = score, 1
        elif score == best:
            count += 1
    return count


# ---- test harness ---------------------------------------------------------

seed = 2049


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(n, reach):
    order = list(range(n))
    for i in range(n - 1, 1, -1):
        j = next_random() % i + 1
        order[i], order[j] = order[j], order[i]
    parents = [-1] * n
    kids = [0] * n
    for i in range(1, n):
        at = i - (next_random() % min(reach, i) + 1)
        while kids[order[at]] == 2:
            at += 1
        parents[order[i]] = order[at]
        kids[order[at]] += 1
    return parents


def show(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def main():
    examples = [
        [-1, 2, 0, 2, 0],
        [-1, 2, 0],
        [-1, 0],
        [-1, 0, 0, 1, 1, 3, 3],
        [-1, 0, 1, 2, 3, 4],
        [-1, 0, 0, 1, 1, 2, 2],
        [-1, 2, 0, 0, 1, 1, 2],
    ]
    for parents in examples:
        print(f"{show(parents)} -> {count_highest_score_nodes(parents)}")
    total = check = 0
    for _ in range(2000):
        n = next_random() % 29 + 2
        reach = next_random() % n + 1
        count = count_highest_score_nodes(draw(n, reach))
        total += count
        check = (check * 31 + count) % 1000000007
    print(f"2000 trees: sum {total}, checksum {check}")
    total = check = 0
    n = 100000
    path = [i - 1 for i in range(n)]
    comb = [-1 if i == 0 else i - 2 if i % 2 == 0 else i - 1 for i in range(n)]
    binary = [-1 if i == 0 else (i - 1) // 2 for i in range(n)]
    rnd = draw(n, n)
    for parents in [path, comb, binary, rnd]:
        count = count_highest_score_nodes(parents)
        total += count
        check = (check * 31 + count) % 1000000007
    print(f"4 trees of 100000 nodes: sum {total}, checksum {check}")


main()
