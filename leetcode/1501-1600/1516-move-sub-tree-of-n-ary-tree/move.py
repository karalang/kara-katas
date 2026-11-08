# LeetCode #1516: Move Sub-Tree of N-Ary Tree -- the Python mirror of the
# ★ arm (move.kara): parent walks from the root, a subtree test, a splice.


class Node:
    def __init__(self, val):
        self.val = val
        self.children = []


def parent_of(node, val):
    for child in node.children:
        if child.val == val:
            return node
        found = parent_of(child, val)
        if found is not None:
            return found
    return None


def contains(node, val):
    if node.val == val:
        return True
    for child in node.children:
        if contains(child, val):
            return True
    return False


def move_sub_tree(root, p, q):
    for child in q.children:
        if child.val == p.val:
            return root
    p_parent = parent_of(root, p.val)
    if contains(p, q.val):
        q_parent = parent_of(root, q.val)
        q_parent.children = [c for c in q_parent.children if c.val != q.val]
        q.children.append(p)
        if p_parent is None:
            return q
        i = next(k for k, c in enumerate(p_parent.children) if c.val == p.val)
        p_parent.children[i] = q
    else:
        p_parent.children = [c for c in p_parent.children if c.val != p.val]
        q.children.append(p)
    return root


def show(node):
    if not node.children:
        return f"{node.val}"
    return f"{node.val}({' '.join(show(c) for c in node.children)})"


def build(vals, parents):
    nodes = [Node(v) for v in vals]
    for i in range(1, len(vals)):
        nodes[parents[i]].children.append(nodes[i])
    return nodes


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def example(p, q):
    nodes = build([1, 2, 3, 4, 5, 6, 7, 8], [0, 0, 0, 1, 1, 2, 3, 3])
    return show(move_sub_tree(nodes[0], nodes[p - 1], nodes[q - 1]))


def batch(count, most, rng):
    check = 0
    for _ in range(count):
        n = rng.next() % (most - 1) + 2
        vals = []
        while len(vals) < n:
            v = rng.next() % 1000 + 1
            if v not in vals:
                vals.append(v)
        parents = [0]
        for i in range(1, n):
            parents.append(rng.next() % i)
        p = rng.next() % n
        q = (p + 1 + rng.next() % (n - 1)) % n
        nodes = build(vals, parents)
        root = move_sub_tree(nodes[0], nodes[p], nodes[q])
        for b in show(root).encode():
            check = mix(check, b)
    return check


def main():
    print(f"example 1, 4 under 1 -> {example(4, 1)}")
    print(f"example 2, 7 under 4 -> {example(7, 4)}")
    print(f"example 3, 3 under 8 -> {example(3, 8)}")
    print(f"2 under its own 7 -> {example(2, 7)}")
    print(f"the root under 8 -> {example(1, 8)}")
    print(f"5 under 2, its parent -> {example(5, 2)}")
    rng = Rng(1516)
    print(f"3000 trees of 2 to 12 nodes: checksum {batch(3000, 12, rng)}")
    print(f"300 trees of 2 to 300 nodes: checksum {batch(300, 300, rng)}")


main()
