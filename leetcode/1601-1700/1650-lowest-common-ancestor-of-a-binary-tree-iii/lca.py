# LeetCode #1650: Lowest Common Ancestor of a Binary Tree III -- the Python
# mirror of the ★ arm: two climbers, each starting over from the other's
# node at the root, meet at the answer.


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


# ---- the harness: the same as every arm's ---------------------------------

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


def find(nodes, val):
    return next(n for n in nodes if n.val == val)


def batch(count, most):
    check = 0
    total = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % (most - 1) + 2
        nodes = random_tree(n)
        for _ in range(5):
            p = next_random() % n
            q = next_random() % n
            if q == p:
                q = (q + 1) % n
            found = lowest_common_ancestor(nodes[p], nodes[q]).val
            total += found
            check = (check * 31 + found + 1) % 1000000007
    print(f"{count} trees of up to {most} nodes: answers sum to {total}, checksum {check}")


example = [Node(v) for v in [3, 5, 1, 6, 2, 0, 8, 7, 4]]
for parent, left, right in [(3, 5, 1), (5, 6, 2), (1, 0, 8), (2, 7, 4)]:
    p = find(example, parent)
    l, r = find(example, left), find(example, right)
    l.parent = p
    r.parent = p
    p.left = l
    p.right = r
print(lowest_common_ancestor(find(example, 5), find(example, 1)).val)
print(lowest_common_ancestor(find(example, 5), find(example, 4)).val)
pair = [Node(1), Node(2)]
pair[1].parent = pair[0]
pair[0].left = pair[1]
print(lowest_common_ancestor(pair[0], pair[1]).val)
print(lowest_common_ancestor(find(example, 2), find(example, 7)).val)
print(lowest_common_ancestor(find(example, 7), find(example, 8)).val)
batch(3000, 8)
batch(300, 1000)
batch(30, 100000)
