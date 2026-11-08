# LeetCode #1506: Find Root of N-Ary Tree -- the benchmark, the
# same algorithm as root.kara: every value but the root's appears once as a child, so the sum of
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


def main():
    trees = [random_tree(50000) for _ in range(20)]
    check = 0
    for _ in range(10):
        for nodes in trees:
            root = find_root(list(nodes))
            check = mix(check, root.val)
    print(f"200 roots over 20 trees of up to 50000 nodes: checksum {check}")


main()
