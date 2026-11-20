# LeetCode #1666: Change the Root of a Binary Tree -- the bench's Python
# mirror: the ★ arm on 30 random trees of 100000 nodes with parent links,
# each turned 50000 times to hang from a leaf reached by a random walk
# down from a random node, the start nodes drawn first.


class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None


def flip_binary_tree(root, leaf):
    cur = leaf
    below = None
    while True:
        above = cur.parent
        cur.parent = below
        if above is None:
            break
        p = above
        if p.left is cur:
            p.left = None
        else:
            p.right = None
        if cur.left is not None:
            cur.right = cur.left
        cur.left = p
        below = cur
        cur = p
    return leaf


# ---- the harness ----------------------------------------------------------

seed = 1666


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
    starts = [next_random() % 100000 for _ in range(50000)]
    trees.append((nodes, starts))
check = 0
steps = 0
for nodes, starts in trees:
    root = nodes[0]
    for s in starts:
        at = nodes[s]
        while True:
            first = at.left if next_random() % 2 == 0 else at.right
            child = first if first is not None else (at.left if at.left is not None else at.right)
            if child is None:
                break
            at = child
            steps += 1
        root = flip_binary_tree(root, at)
        check = (check * 31 + root.val + 1) % 1000000007
print(f"30 trees of 100000 nodes, 50000 turns each: {steps} steps down, checksum {check}")
