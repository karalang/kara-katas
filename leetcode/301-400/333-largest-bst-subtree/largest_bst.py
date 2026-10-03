# LeetCode #333: Largest BST Subtree — one post-order pass.
# Python mirror of largest_bst.kara; prints the same lines.
import sys

sys.setrecursionlimit(100000)

NULL = -1000000007


def visit(nodes, node, best):
    val, left, right = nodes[node]
    bst, size, lo, hi = True, 1, val, val
    if left != -1:
        lb, ls, llo, lhi = visit(nodes, left, best)
        if lb and lhi < val:
            size += ls
            lo = llo
        else:
            bst = False
    if right != -1:
        rb, rs, rlo, rhi = visit(nodes, right, best)
        if rb and rlo > val:
            size += rs
            hi = rhi
        else:
            bst = False
    if bst and size > best[0]:
        best[0] = size
    return bst, size, lo, hi


def largest_bst_subtree(nodes):
    if not nodes:
        return 0
    best = [0]
    visit(nodes, 0, best)
    return best[0]


def build(vals):
    nodes = []
    if not vals or vals[0] == NULL:
        return nodes
    nodes.append([vals[0], -1, -1])
    queue = [0]
    head, i = 0, 1
    while head < len(queue) and i < len(vals):
        cur = queue[head]
        head += 1
        if vals[i] != NULL:
            nodes.append([vals[i], -1, -1])
            nodes[cur][1] = len(nodes) - 1
            queue.append(len(nodes) - 1)
        i += 1
        if i < len(vals) and vals[i] != NULL:
            nodes.append([vals[i], -1, -1])
            nodes[cur][2] = len(nodes) - 1
            queue.append(len(nodes) - 1)
        i += 1
    return nodes


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def insert(nodes, v):
    nodes.append([v, -1, -1])
    nid = len(nodes) - 1
    cur = 0
    while cur != nid:
        if v < nodes[cur][0]:
            if nodes[cur][1] == -1:
                nodes[cur][1] = nid
            cur = nodes[cur][1]
        else:
            if nodes[cur][2] == -1:
                nodes[cur][2] = nid
            cur = nodes[cur][2]


def random_tree(rng, n, rng_range, damage):
    nodes = []
    for _ in range(n):
        a = rng.next()
        b = rng.next()
        insert(nodes, (a * 32768 + b) % rng_range)
    for _ in range(damage):
        at = rng.next() % n
        a = rng.next()
        b = rng.next()
        nodes[at][0] = (a * 32768 + b) % rng_range
    return nodes


def show(vals):
    nodes = build(vals)
    shown = ",".join("null" if v == NULL else str(v) for v in vals)
    print(f"[{shown}] -> {largest_bst_subtree(nodes)}")


def main():
    show([10, 5, 15, 1, 8, NULL, 7])
    show([4, 2, 7, 2, 3, 5, NULL, 2, NULL, NULL, NULL, NULL, NULL, 1])
    show([])
    show([1])
    show([2, 2, 2])
    show([2, 1, 3])
    show([1, 2, 3])
    show([3, 2, NULL, 1])
    show([1, NULL, 2, NULL, 3])
    show([10, 5, 15, 1, 12, NULL, 20])
    show([5, 3, 8, 1, 4, 7, 9, NULL, NULL, NULL, NULL, 6])
    show([-9223372036854775808, NULL, 9223372036854775807])
    rng = Rng(333)
    for rnd in range(6):
        n = 5 + rnd * 7
        nodes = random_tree(rng, n, 4 * n, rnd % 3)
        print(f"random {rnd}: {n} nodes -> {largest_bst_subtree(nodes)}")
    big = random_tree(rng, 20000, 1000000000, 0)
    damaged = random_tree(rng, 20000, 1000000000, 40)
    print(f"big: {len(big)} nodes -> {largest_bst_subtree(big)}, 40 damaged -> {largest_bst_subtree(damaged)}")


main()
