# LeetCode #1506: Find Root of N-Ary Tree -- the Python mirror of the ★
# arm: every value but the root's appears once as a child, so the sum of
# all values less the sum of all children's values is the root's.


class Node:
    def __init__(self, val, children):
        self.val = val
        self.children = children


def find_root(nodes):
    total = 0
    for node in nodes:
        total += node.val
        for child in node.children:
            total -= child.val
    for node in nodes:
        if node.val == total:
            return node
    return None


# A tree from LeetCode's level-order form: the root, a None, then each
# node's children followed by a None, in level order.
def from_level_order(tokens):
    vals = [tokens[0]]
    kids = [[]]
    parent = 0
    for t in tokens[2:]:
        if t is None:
            parent += 1
        else:
            kids[parent].append(len(vals))
            vals.append(t)
            kids.append([])
    nodes = [None] * len(vals)
    for i in range(len(vals) - 1, -1, -1):
        nodes[i] = Node(vals[i], [nodes[c] for c in kids[i]])
    return nodes


seed = 1506


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


# 1 to `most` nodes with distinct values in 0..=50000, each node after the
# first the child of an earlier one, built leaves first, then shuffled.
def random_tree(most):
    n = next_random() % most + 1
    vals = []
    seen = set()
    while len(vals) < n:
        v = (next_random() * 65536 + next_random()) % 50001
        if v not in seen:
            seen.add(v)
            vals.append(v)
    kids = [[] for _ in range(n)]
    for i in range(1, n):
        kids[next_random() % i].append(i)
    nodes = [None] * n
    for i in range(n - 1, -1, -1):
        nodes[i] = Node(vals[i], [nodes[c] for c in kids[i]])
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        nodes[i], nodes[j] = nodes[j], nodes[i]
    return nodes


def batch(count, most):
    check = 0
    for _ in range(count):
        root = find_root(random_tree(most))
        check = mix(check, root.val)
    print(f"{count} trees of 1 to {most} nodes: checksum {check}")


def main():
    examples = [
        [1, None, 3, 2, 4, None, 5, 6],
        [1, None, 2, 3, 4, 5, None, None, 6, 7, None, 8, None, 9, 10, None, None, 11, None, 12, None, 13, None, None, 14],
        [7],
        [5, None, 9, None, 0],
    ]
    for tokens in examples:
        nodes = from_level_order(tokens)
        nodes = nodes[::-1]
        root = find_root(nodes)
        print(f"{len(nodes)} nodes, listed leaves first -> root {root.val} with {len(root.children)} children")
    batch(3000, 10)
    batch(300, 300)
    batch(3, 50000)


main()
