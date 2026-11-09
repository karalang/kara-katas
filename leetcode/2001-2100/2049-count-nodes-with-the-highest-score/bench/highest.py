# LeetCode #2049: Count Nodes With the Highest Score -- Python mirror of the
# ★ arm's benchmark (highest.kara): the same 50 trees of 100000 nodes, the
# same explicit-stack preorder walked backwards.

seed = 2049


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(n, reach):
    parents = [-1] * n
    kids = [0] * n
    for i in range(1, n):
        at = i - (next_random() % min(reach, i) + 1)
        while kids[at] == 2:
            at += 1
        parents[i] = at
        kids[at] += 1
    return parents


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


def main():
    total = check = 0
    for t in range(50):
        count = count_highest_score_nodes(draw(100000, 1 + t * 1000))
        total += count
        check = (check * 31 + count) % 1000000007
    print(f"50 trees: sum {total}, checksum {check}")


main()
