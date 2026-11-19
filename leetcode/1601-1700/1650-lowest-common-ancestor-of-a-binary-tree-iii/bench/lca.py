# LeetCode #1650: Lowest Common Ancestor of a Binary Tree III -- the
# bench's Python mirror: the ★ arm on 30 random trees of 100000 nodes with
# parent links, each asked about 50000 pairs of its nodes, all drawn
# first.


class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None


def lowest_common_ancestor(p, q):
    a, b = p, q
    while a.val != b.val:
        a = a.parent if a.parent is not None else q
        b = b.parent if b.parent is not None else p
    return a


# ---- the harness ----------------------------------------------------------

seed = 1650


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_tree(n):
    values = list(range(n))
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        values[i], values[j] = values[j], values[i]
    nodes = []
    for i in range(n):
        node = Node(values[i])
        if i > 0:
            at = nodes[next_random() % i]
            while True:
                if next_random() % 2 == 0:
                    if at.left is not None:
                        at = at.left
                    else:
                        node.parent = at
                        at.left = node
                        break
                else:
                    if at.right is not None:
                        at = at.right
                    else:
                        node.parent = at
                        at.right = node
                        break
        nodes.append(node)
    return nodes


trees = []
for _ in range(30):
    nodes = random_tree(100000)
    pairs = []
    for _ in range(50000):
        p = next_random() % 100000
        q = next_random() % 100000
        if q == p:
            q = (q + 1) % 100000
        pairs.append((p, q))
    trees.append((nodes, pairs))
check = 0
total = 0
for nodes, pairs in trees:
    for p, q in pairs:
        found = lowest_common_ancestor(nodes[p], nodes[q]).val
        total += found
        check = (check * 31 + found + 1) % 1000000007
print(f"30 trees of 100000 nodes, 50000 pairs each: answers sum to {total}, checksum {check}")
