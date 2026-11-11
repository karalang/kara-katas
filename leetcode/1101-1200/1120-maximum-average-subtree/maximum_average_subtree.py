# LeetCode #1120: Maximum Average Subtree -- Python mirror of the ★ arm.
import sys

sys.setrecursionlimit(100000)


class TreeNode:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def walk(node, best):
    if node is None:
        return 0, 0
    ls, lc = walk(node.left, best)
    rs, rc = walk(node.right, best)
    s = ls + rs + node.val
    c = lc + rc + 1
    a = s / c
    if a > best[0]:
        best[0] = a
    return s, c


def maximum_average_subtree(root):
    best = [0.0]
    walk(root, best)
    return best[0]


seed = 1120


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


def random_tree(size, top):
    root = TreeNode((next_random() * 32768 + next_random()) % (top + 1))
    nodes = [root]
    for _ in range(1, size):
        v = (next_random() * 32768 + next_random()) % (top + 1)
        while True:
            at = nodes[next_random() % len(nodes)]
            if next_random() % 2 == 0:
                if at.left is None:
                    at.left = TreeNode(v)
                    nodes.append(at.left)
                    break
            elif at.right is None:
                at.right = TreeNode(v)
                nodes.append(at.right)
                break
    return root


def main():
    cases = ["[5,6,1]", "[0,null,1]", "[7]", "[0,0,0]", "[1,2,3,4,5,6,100000]", "[10,1,1]", "[1,null,2,null,3,null,4]", "[3,9,20,null,null,15,7]"]
    for text in cases:
        print(f"{text} -> {maximum_average_subtree(parse(text)):.5f}")
    total = 0.0
    check = 0
    for i in range(2000):
        size = next_random() % 40 + 1
        top = [10, 1000, 100000][i % 3]
        answer = maximum_average_subtree(random_tree(size, top))
        total += answer
        for b in f"{answer:.5f}".encode():
            check = (check * 131 + b) % 1000000007
    print(f"2000 random trees: answers total {total:.3f}, checksum {check}")
    big = random_tree(10000, 100000)
    print(f"10^4 random nodes: {maximum_average_subtree(big):.5f}")
    chain = ["100000" if i == 0 else f"null,{100000 - i * 10}" for i in range(10000)]
    print(f"a chain of 10^4: {maximum_average_subtree(parse('[' + ','.join(chain) + ']')):.5f}")


main()
