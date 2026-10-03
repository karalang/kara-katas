# LeetCode #337: House Robber III — Python mirror of house_robber_iii.kara.
#
# Same post-order over the same index pool, the same harness and the same
# output. The recursion limit is raised for the 10,000-house chain.

import sys

sys.setrecursionlimit(100000)

NULL = -1000000007


def visit(nodes, node):
    if node == -1:
        return (0, 0)
    lr, ls = visit(nodes, nodes[node][1])
    rr, rs = visit(nodes, nodes[node][2])
    return (nodes[node][0] + ls + rs, max(lr, ls) + max(rr, rs))


def rob(nodes):
    if not nodes:
        return 0
    r, s = visit(nodes, 0)
    return max(r, s)


def build(vals):
    nodes = []
    if not vals or vals[0] == NULL:
        return nodes
    nodes.append([vals[0], -1, -1])
    queue = [0]
    head = 0
    i = 1
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


def random_tree(rng, n, most):
    nodes = []
    for i in range(n):
        nodes.append([rng.next() % (most + 1), -1, -1])
        if i == 0:
            continue
        cur = 0
        while True:
            if rng.next() % 2 == 0:
                if nodes[cur][1] == -1:
                    nodes[cur][1] = i
                    break
                cur = nodes[cur][1]
            else:
                if nodes[cur][2] == -1:
                    nodes[cur][2] = i
                    break
                cur = nodes[cur][2]
    return nodes


def chain(n):
    nodes = []
    for i in range(n):
        nodes.append([i + 1, -1, -1])
        if i > 0:
            if i % 2 == 0:
                nodes[i - 1][1] = i
            else:
                nodes[i - 1][2] = i
    return nodes


def show(vals):
    nodes = build(vals)
    shown = ",".join("null" if v == NULL else str(v) for v in vals)
    print(f"[{shown}] -> {rob(nodes)}")


def main():
    show([3, 2, 3, NULL, 3, NULL, 1])
    show([3, 4, 5, 1, 3, NULL, 1])
    show([])
    show([0])
    show([7])
    show([1, 2])
    show([2, 1, 1])
    show([1, 2, 3])
    show([4, 1, NULL, 2, NULL, 3])
    show([2, 1, 3, NULL, 4])
    show([0, 0, 0, 0, 0])
    show([10, 1, 1, 10, 10, 10, 10])
    rng = Rng(337)
    for rnd in range(6):
        n = 3 + rnd * 5
        nodes = random_tree(rng, n, 10)
        print(f"random {rnd}: {n} houses -> {rob(nodes)}")
    big = random_tree(rng, 10000, 10000)
    line = chain(10000)
    print(f"big: {len(big)} houses -> {rob(big)}, chain of {len(line)} -> {rob(line)}")


main()
