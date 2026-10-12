# LeetCode #429: N-ary Tree Level Order Traversal -- mirror of
# level_order.kara (breadth first, a level at a time).


class Node:
    def __init__(self, val, children=None):
        self.val = val
        self.children = children if children is not None else []


def level_order(root):
    levels = []
    level = [root] if root is not None else []
    while level:
        row = []
        nxt = []
        for node in level:
            row.append(node.val)
            nxt.extend(node.children)
        levels.append(row)
        level = nxt
    return levels


# ---- test harness ---------------------------------------------------------


def leaf(val):
    return Node(val)


def tree(val, children):
    return Node(val, children)


def show(levels):
    return "[" + ",".join("[" + ",".join(str(v) for v in row) + "]" for row in levels) + "]"


seed = 429


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def build_random(i, vals, kids):
    return Node(vals[i], [build_random(k, vals, kids) for k in kids[i]])


def random_tree(n):
    if n == 0:
        return None
    vals = []
    kids = []
    reach = 1 + step() % n
    for i in range(n):
        vals.append(step() % 10001)
        kids.append([])
        if i > 0:
            back = 1 + step() % min(i, reach)
            kids[i - back].append(i)
    return build_random(0, vals, kids)


def main():
    print(show(level_order(tree(1, [tree(3, [leaf(5), leaf(6)]), leaf(2), leaf(4)]))))
    print(show(level_order(tree(1, [
        leaf(2),
        tree(3, [leaf(6), tree(7, [tree(11, [leaf(14)])])]),
        tree(4, [tree(8, [leaf(12)])]),
        tree(5, [tree(9, [leaf(13)]), leaf(10)]),
    ]))))
    print(show(level_order(None)))
    print(show(level_order(leaf(7))))
    print(show(level_order(tree(1, [tree(2, [tree(3, [tree(4, [leaf(5)])])])]))))
    print(show(level_order(tree(100, [leaf(v * 7) for v in range(12)]))))
    print(show(level_order(tree(0, [leaf(1), tree(2, [leaf(4)]), tree(3, [tree(5, [leaf(6)])])]))))
    nodes = 0
    depth = 0
    checksum = 0
    for _ in range(300):
        n = step() % 61
        levels = level_order(random_tree(n))
        nodes += n
        depth += len(levels)
        for b in show(levels).encode():
            checksum = (checksum * 31 + b) % 1000000007
    print(f"300 random trees, {nodes} nodes, {depth} levels: checksum {checksum}")


main()
