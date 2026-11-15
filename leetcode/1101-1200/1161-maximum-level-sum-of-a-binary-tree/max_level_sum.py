# LeetCode #1161: Maximum Level Sum of a Binary Tree -- a Python mirror
# of the ★ arm: level by level, a level taking the lead only with a
# strictly larger sum. Its output is byte-identical to max_level_sum.kara.


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val, self.left, self.right = val, None, None


def max_level_sum(root):
    level = [root] if root else []
    best = best_sum = depth = 0
    while level:
        depth += 1
        total = 0
        nxt = []
        for node in level:
            total += node.val
            if node.left:
                nxt.append(node.left)
            if node.right:
                nxt.append(node.right)
        if best == 0 or total > best_sum:
            best, best_sum = depth, total
        level = nxt
    return best


# ---- test harness ---------------------------------------------------------

class Seed:
    def __init__(self, s):
        self.s = s

    def next(self):
        self.s = (self.s * 1103515245 + 12345) % 2147483648
        return self.s // 65536


def parse(text):
    inner = text[1:-1]
    if not inner:
        return None
    items = [None if s == "null" else int(s) for s in inner.split(",")]
    root = TreeNode(items[0])
    queue = [root]
    head = 0
    i = 1
    while i < len(items):
        node = queue[head]
        head += 1
        if items[i] is not None:
            node.left = TreeNode(items[i])
            queue.append(node.left)
        i += 1
        if i < len(items):
            if items[i] is not None:
                node.right = TreeNode(items[i])
                queue.append(node.right)
            i += 1
    return root


def value(seed, small):
    return seed.next() % 5 - 2 if small else seed.next() % 200001 - 100000


def random_tree(seed, count, deep, small):
    root = TreeNode(value(seed, small))
    nodes = [root]
    for _ in range(1, count):
        c = TreeNode(value(seed, small))
        while True:
            if deep and seed.next() % 2 == 0:
                at = nodes[-1]
            else:
                at = nodes[seed.next() % len(nodes)]
            if seed.next() % 2 == 0:
                if at.left is None:
                    at.left = c
                    break
            elif at.right is None:
                at.right = c
                break
        nodes.append(c)
    return root


def main(f=max_level_sum):
    cases = [
        "[1,7,0,7,-8,null,null]",
        "[989,null,10250,98693,-89388,null,null,null,-32127]",
        "[5]",
        "[-1,-2,-3]",
        "[1,1,0]",
        "[0,0,0,0]",
        "[-5,-1,-1]",
        "[1,2,null,3,null,4,null,5]",
    ]
    for c in cases:
        print(f"{c} -> {f(parse(c))}")
    seed = Seed(1161)
    levels = check = 0
    for t in range(1000):
        count = seed.next() % 1000 + 1
        root = random_tree(seed, count, t % 4 == 1, t % 2 == 0)
        level = f(root)
        levels += level
        check = (check * 31 + level) % 1000000007
    print(f"1000 random trees: levels {levels}, checksum {check}")
    for deep in [False, True]:
        root = random_tree(seed, 10000, deep, False)
        print(f"10000 nodes: level {f(root)}")


if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(100000)
    main()
